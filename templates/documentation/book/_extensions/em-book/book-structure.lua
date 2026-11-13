-- Book structure for the Typst template. Reads the parts from `book.chapters`, inserts a
-- part title page before the first chapter of a part and a break to the next right-hand
-- page before every other chapter. Also keeps pictures and lead-in sentences from leaving
-- half-empty pages, and repairs German closing quotation marks.
local function raw(code) return pandoc.RawBlock("typst", code) end
local function typst_string(s) return '"' .. s:gsub("\\", "\\\\"):gsub('"', '\\"') .. '"' end
local function text_of(value) return value and pandoc.utils.stringify(value) or nil end

-- file -> {index, title} from Quarto's flattened chapter list.
local function parts_by_file(meta)
  local result, current, count = {}, nil, 0
  local items = meta.book and meta.book.render or {}
  for _, item in ipairs(items) do
    local kind = text_of(item.type)
    if kind == "part" then
      count = count + 1
      current = { index = count, title = text_of(item.text) or text_of(item.file) or "" }
    elseif kind == "chapter" and item.file then
      if text_of(item.depth) == "0" then current = nil end
      result[text_of(item.file)] = current
    end
  end
  return result
end

-- Width and height in pixels of a PNG below one of the candidate directories.
local function png_size(src, dirs)
  for _, dir in ipairs(dirs) do
    local f = io.open(pandoc.path.join({ dir, src }), "rb")
    if f then
      local head = f:read(24); f:close()
      if head and #head == 24 and head:sub(2, 4) == "PNG" then
        return string.unpack(">I4", head, 17), string.unpack(">I4", head, 21)
      end
    end
  end
end

-- A closing quotation mark typed as " or “ after an opening „ reaches Typst as a plain ",
-- which Typst then sets as another opening „. Emit the closing mark itself instead.
local function closing_quotes(inlines)
  local result, open = pandoc.List(), false
  for _, el in ipairs(inlines) do
    if el.t == "Str" and (el.text:find('"', 1, true) or el.text:find("“", 1, true) or el.text:find("”", 1, true) or el.text:find("„", 1, true)) then
      local buffer = ""
      local function flush()
        if buffer ~= "" then result:insert(pandoc.Str(buffer)); buffer = "" end
      end
      for _, code in utf8.codes(el.text) do
        local ch = utf8.char(code)
        if ch == "„" then
          open = true; buffer = buffer .. ch
        elseif ch == '"' or ch == "“" or ch == "”" then
          if open or buffer ~= "" then
            flush(); result:insert(pandoc.RawInline("typst", "“")); open = false
          else
            buffer = buffer .. ch
          end
        else
          buffer = buffer .. ch
        end
      end
      flush()
    elseif el.t == "Quoted" and el.quotetype == "DoubleQuote" and open then
      -- Pandoc paired the closing mark of „A" with the closing mark of a later „B".
      result:insert(pandoc.RawInline("typst", "“"))
      result:extend(el.content)
      result:insert(pandoc.RawInline("typst", "“"))
      open = false
    else
      result:insert(el)
    end
  end
  return result
end

return {{
  Pandoc = function(doc)
    local meta = doc.meta
    local parts = parts_by_file(meta)
    local german = (text_of(meta.lang) or "en"):match("^de") ~= nil
    -- Text block of typst-template.typ: 210 mm less 32 mm and 24 mm margins.
    local text_width = 154
    local max_height = tonumber(text_of(meta["image-max-height"]) or "") or 118
    local widths = {}
    if type(meta["image-widths"]) == "table" then
      for file, width in pairs(meta["image-widths"]) do widths[file] = text_of(width) end
    end

    local resource_dir = "."
    local function fit_image(el)
      local file = el.src:match("([^/]+)$")
      if widths[file] then el.attributes.width = widths[file]; return el end
      -- A picture taller than about half the text block rarely fits the rest of a page and
      -- leaves it half empty. Narrow such a picture until it is at most max_height tall.
      local w, h = png_size(el.src, { resource_dir, "." })
      if w and h then
        local width = tonumber((el.attributes.width or "100%"):match("^([%d.]+)mm$"))
        if not width then
          local percent = tonumber((el.attributes.width or "100%"):match("^([%d.]+)%%$"))
          width = percent and text_width * percent / 100
        end
        if width and width * h / w > max_height then
          el.attributes.width = string.format("%.1fmm", max_height * w / h)
        end
      end
      return el
    end

    local blocks, opening, file, in_part = pandoc.List(), false, nil, nil
    for _, block in ipairs(doc.blocks) do
      local encoded = block.t == "RawBlock" and block.text:match("quarto%-file%-metadata: (%S+)")
      if encoded then
        local info = quarto.json.decode(quarto.base64.decode(encoded))
        if info.bookItemType == "chapter" then
          file, opening, resource_dir = info.bookItemFile, true, info.resourceDir or "."
        end
        blocks:insert(block)
      elseif block.t == "Div" and block.classes:includes("quarto-book-part") then
        -- Quarto's own part heading; em-part() sets the part title page instead.
      elseif block.t == "Header" and block.level == 1 and pandoc.utils.stringify(block.content):match("^%s*$") then
        -- An empty title, as in an index.md that only carries metadata.
      elseif block.t == "Header" and block.level == 1 and opening then
        opening = false
        local part = parts[file]
        if part and part.index ~= in_part then
          blocks:insert(raw("#em-part(" .. part.index .. ", " .. typst_string(part.title) .. ")"))
        elseif not part and in_part then
          blocks:insert(raw("#em-chapter-break(reset: true)"))
        else
          blocks:insert(raw("#em-chapter-break()"))
        end
        in_part = part and part.index or nil
        blocks:insert(block)
      else
        blocks:insert(block:walk({ Image = fit_image }))
      end
    end

    -- Keep a lead-in sentence ("…:") on the page of the table, list or picture it announces.
    local kept = pandoc.List()
    for i, block in ipairs(blocks) do
      local nxt = blocks[i + 1]
      if block.t == "Para" and nxt and (nxt.t == "Table" or nxt.t == "BulletList" or nxt.t == "OrderedList"
          or (nxt.t == "Para" and #nxt.content == 1 and nxt.content[1].t == "Image"))
          and pandoc.utils.stringify(block.content):match(":%s*$") then
        kept:insert(raw("#block(sticky: true)["))
        kept:insert(block)
        kept:insert(raw("]"))
      else
        kept:insert(block)
      end
    end
    doc.blocks = kept
    if german then doc = doc:walk({ Inlines = closing_quotes }) end
    return doc
  end,
}}
