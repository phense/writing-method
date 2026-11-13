// Book layout for duplex printing and binding: mirrored margins, a running head with the
// part name on a grey band next to the chapter, part title pages, chapters opening on a
// right-hand page. Quarto supplies document conversion, callouts and cross-references.
//
// book-structure.lua reads the parts from `book.chapters` and inserts em-part() before the
// first chapter of a part and em-chapter-break() before every other chapter.
#let em-accent = state("em-accent", rgb("173A5E"))
#let em-part-label = state("em-part-label", "Part")
// Part of the current chapter: none or (index: 1, title: "…").
#let em-part-state = state("em-part", none)
#let em-band = luma(232)

#let em-chapters() = query(heading.where(level: 1, outlined: true))
#let em-chapter-number(h) = if h.numbering != none { str(counter(heading).at(h.location()).first()) }

// Closes the previous chapter and moves to the next right-hand page. The marker lets header
// and footer leave the resulting empty left-hand page blank. `reset` ends the current part
// for a chapter that is listed after a part but outside of one.
#let em-chapter-break(reset: false) = {
  [#metadata("end") <em-end>]
  pagebreak(to: "odd", weak: true)
  if reset { em-part-state.update(none) }
}

// Title page of a part, followed by its first chapter on the next right-hand page.
#let em-part(index, title) = {
  [#metadata("end") <em-end>]
  pagebreak(to: "odd", weak: true)
  context page(fill: em-accent.get(), header: none, footer: none)[
    #metadata("part") <em-end>
    #set text(fill: white, hyphenate: false)
    #set par(justify: false)
    #v(42mm)
    #text(size: 13pt, fill: white.transparentize(25%), tracking: 0.1em, weight: "semibold",
      upper[#em-part-label.get() #index])
    #v(4mm)
    #text(size: 40pt, weight: "bold", title)
    #v(10mm)
    #set text(size: 11pt)
    #show link: set text(fill: white)
    #for h in em-chapters().filter(h => {
      let part = em-part-state.at(h.location())
      part != none and part.index == index
    }) {
      block(above: 0.66em, link(h.location(), grid(columns: (9mm, 1fr, auto),
        em-chapter-number(h), h.body, str(counter(page).at(h.location()).first()))))
    }
  ]
  pagebreak(to: "odd", weak: true)
  em-part-state.update((index: index, title: title))
}

#let em-book(
  title: [], subtitle: [], lang: "en", kind: [], part-label: "", font: ("Source Sans 3",),
  font-size: 11pt, code-font: ("DejaVu Sans Mono",), code-size: 9.5pt, show-toc: true,
  toc-title: [], numbering-pattern: "1.1",
  imprint-version: [], imprint-date: "", imprint-organisation: (), imprint-author: (),
  accent: rgb("173A5E"), ink: rgb("232A31"), muted: rgb("5B6670"), body,
) = {
  let german = lang.starts-with("de")
  let kind = if kind != [] { kind } else if german { [Handbuch] } else { [Manual] }
  em-accent.update(accent)
  em-part-label.update(if part-label != "" { part-label } else if german { "Teil" } else { "Part" })
  set document(title: title)
  set text(font: font, size: font-size, fill: ink, lang: lang, hyphenate: true)
  set par(justify: false, leading: 0.72em, spacing: 1.05em, linebreaks: "optimized")
  set heading(numbering: numbering-pattern)
  show heading: set text(font: font, hyphenate: false)
  set list(indent: 0.4em, body-indent: 0.7em, spacing: 0.75em)
  set enum(indent: 0.4em, body-indent: 0.7em, spacing: 0.75em)

  // What the running head of page p shows; none on title, part, chapter-opening and
  // empty pages.
  let running(p) = {
    let ends = query(<em-end>)
    let hs = query(heading.where(level: 1))
    if p == 1 or ends.any(m => m.value == "part" and m.location().page() == p) { return none }
    // An empty left-hand page: the next page opens a chapter or part and no chapter ended here.
    let opens-next = hs.any(h => h.location().page() == p + 1) or ends.any(m => m.value == "part" and m.location().page() == p + 1)
    if calc.even(p) and opens-next and not ends.any(m => m.value == "end" and m.location().page() == p) { return (empty: true) }
    if hs.any(h => h.location().page() == p) { return none }
    let before = hs.filter(h => h.location().page() < p)
    if before.len() == 0 { return none }
    let h = before.last()
    let part = em-part-state.at(h.location())
    (part: if part != none and h.outlined { part.title }, number: em-chapter-number(h), title: h.body)
  }
  let pageno() = text(weight: "semibold", fill: ink, str(counter(page).get().first()))
  let tag(body) = box(fill: em-band, inset: (x: 3.2mm, y: 2mm), radius: 1pt,
    text(size: 8.2pt, fill: accent, weight: "semibold", tracking: 0.09em, upper(body)))

  set page(
    margin: (inside: 32mm, outside: 24mm, top: 30mm, bottom: 27mm),
    header-ascent: 9mm,
    footer-descent: 9mm,
    header: context {
      let p = here().page()
      let c = running(p)
      if c == none or "empty" in c { return }
      set text(size: 8.6pt, fill: ink, hyphenate: false)
      let chapter = if c.number != none [#c.number #h(0.4em) #c.title] else { c.title }
      let label = if c.part != none { tag(c.part) }
      let number = box(inset: (y: 2mm), pageno())
      if calc.odd(p) {
        grid(columns: (auto, 1fr, auto), gutter: 3.5mm,
          align: (left + horizon, left + horizon, right + horizon), label, chapter, number)
      } else {
        grid(columns: (auto, 1fr, auto), gutter: 3.5mm,
          align: (left + horizon, right + horizon, right + horizon), number, chapter, label)
      }
      v(-2.6mm)
      line(length: 100%, stroke: 0.8pt + em-band)
    },
    footer: context {
      let p = here().page()
      let c = running(p)
      if p == 1 or (c != none and "empty" in c) { return }
      if query(<em-end>).any(m => m.value == "part" and m.location().page() == p) { return }
      set text(size: 8.6pt, fill: muted)
      // Pages with a running head carry the page number there; the others carry it here.
      if c == none { align(if calc.odd(p) { right } else { left }, pageno()) }
      else { align(if calc.odd(p) { left } else { right }, text(size: 7.8pt, title)) }
    },
  )

  show link: set text(fill: accent)
  show raw: set text(font: code-font, size: code-size)
  show raw.where(block: true): set text(hyphenate: false)
  show raw.where(block: true): it => block(width: 100%, fill: luma(246), inset: 8pt, radius: 2pt, breakable: true, it)
  show image: it => box(stroke: 0.5pt + luma(190), radius: 1.5pt, clip: true, it)
  set table(
    inset: (x: 5.5pt, y: 5pt),
    stroke: (x, y) => (top: if y == 0 { 0.9pt + ink } else { 0.35pt + luma(185) }, bottom: 0.9pt + ink),
    fill: (x, y) => if y == 0 { luma(238) } else { none },
  )
  show table: set text(size: 9.6pt, hyphenate: true)
  show table: set par(justify: false, leading: 0.6em)
  show table.cell.where(y: 0): set text(weight: "semibold")

  show heading.where(level: 1): it => {
    if it.numbering == none {
      block(above: 0mm, below: 9mm, text(size: 24pt, weight: "bold", it.body))
      return
    }
    context {
      let part = em-part-state.get()
      block(above: 0mm, below: 9mm, width: 100%, sticky: true)[
        #if part != none { tag(part.title) }
        #v(2mm)
        #grid(columns: (auto, 1fr), gutter: 5mm, align: (left + top, left + horizon),
          box(fill: accent, inset: (x: 4mm, y: 3.2mm), radius: 1.5pt,
            text(size: 24pt, weight: "bold", fill: white, counter(heading).display("1"))),
          par(leading: 0.5em, justify: false, text(size: 24pt, weight: "bold", it.body)))
      ]
    }
  }
  show heading.where(level: 2): set text(size: 14.5pt, weight: "bold", fill: accent)
  show heading.where(level: 2): set block(above: 22pt, below: 11pt, sticky: true)
  show heading.where(level: 3): set text(size: 11.6pt, weight: "bold")
  show heading.where(level: 3): set block(above: 18pt, below: 9pt, sticky: true)
  show quote.where(block: true): it => block(
    width: 100%, inset: 10pt, fill: luma(244), stroke: (left: 2pt + accent), it.body)

  // Title page; its back carries the imprint so the contents start on a right-hand page.
  page(header: none, footer: none, margin: (left: 32mm, right: 24mm, top: 30mm, bottom: 27mm))[
    #place(top + left, dx: -32mm, dy: -30mm, rect(width: 210mm, height: 112mm, fill: accent))
    #set par(justify: false)
    #v(46mm)
    #text(size: 10pt, weight: "semibold", tracking: 0.14em, fill: white.transparentize(20%), upper(kind))
    #v(5mm)
    #par(leading: 0.3em, text(size: 40pt, weight: "bold", fill: white, title))
    #v(34mm)
    #line(length: 34mm, stroke: 1.4pt + accent)
    #v(4mm)
    #block(width: 80%, text(size: 13pt, fill: muted, subtitle))
    #metadata("end") <em-end>
  ]
  if imprint-organisation.len() > 0 or imprint-author.len() > 0 {
    page(header: none, footer: none)[
      #set par(justify: false, leading: 0.62em, spacing: 0.62em)
      #set text(size: 10pt)
      #v(1fr)
      #text(size: 13pt, weight: "bold", title)
      #v(1.5mm)
      #kind
      #if imprint-version != [] [v#imprint-version]
      #if imprint-date != "" { linebreak(); if german [Stand: ] else [As of: ]; imprint-date }
      #v(7mm)
      #text(size: 8.2pt, fill: accent, weight: "semibold", tracking: 0.09em, if german { "AUTOR" } else { "AUTHOR" })
      #v(1.5mm)
      #for (i, item) in imprint-organisation.enumerate() { if i == 0 { strong(item) } else { item }; linebreak() }
      #v(3mm)
      #for item in imprint-author { item; linebreak() }
    ]
  }
  pagebreak(to: "odd", weak: true)
  if show-toc {
    heading(level: 1, numbering: none, outlined: false,
      if toc-title != [] { toc-title } else if german { [Inhaltsverzeichnis] } else { [Contents] })
    set text(size: 10pt)
    context {
      let previous = none
      for h in em-chapters() {
        let part = em-part-state.at(h.location())
        if part != none and part.index != previous {
          block(above: 5.5mm, below: 2.2mm, sticky: true, tag(part.title))
          previous = part.index
        }
        block(above: 0.62em, link(h.location(), grid(columns: (8mm, auto, 1fr, auto), gutter: 1.5mm,
          text(fill: muted, em-chapter-number(h)), text(fill: ink, h.body),
          box(width: 1fr, text(fill: luma(170), repeat(gap: 2.5pt)[.])),
          text(fill: ink, str(counter(page).at(h.location()).first())))))
      }
    }
  }
  body
}
