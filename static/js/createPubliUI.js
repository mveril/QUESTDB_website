function createPubliUI(publi,sets=new Map(),toolTips=false) {
  const art = $("<article/>").addClass("publi")
  art.className = "publi"
  if (sets.has(publi.DOI) && sets.get(publi.DOI)!==null) {
    $("<header/>").append($("<h1/>").text(sets.get(publi.DOI))).appendTo(art)  
  }
  $("<a/>", {
    href: publi.URL,
    target: "_blank"
  }).html($("<h2/>").text(publi.title)).appendTo(art)
  const authors = publi.author
  const ulauthors = $("<ul/>").addClass("authors-list").appendTo(art)
  for (const author of authors) {
    const liauth = $("<li/>").addClass("author-item")
    const spanAuth = $("<span/>").text(String.raw`${author.given} ${author.family}`).appendTo(liauth)
    if (author.sequence === "first") {
      $(spanAuth).after($("<strong/>").text("*"))
    }
    var notifycontent = $("<div/>").addClass("author-info")
    $("<h1/>").text(String.raw`${author.given} ${author.family}`).appendTo(notifycontent)
    ulaff = $("<ul/>").addClass("affiliation-list").appendTo(notifycontent)
    for (const a of author.affiliation) {
      $("<li/>").text(a.name).appendTo(ulaff)
    }
    if (author["authenticated-orcid"]) {
      const html = String.raw`<div class="orcid-id"><a href="https://orcid.org" target="_blank"><img alt="ORCID logo" src="https://orcid.org/sites/default/files/images/orcid_16x16.png" width="16" height="16"/></a> <a href="${author.ORCID}" target="_blank">${author.ORCID} </a></div>`
      notifycontent.append(html)
    }
    if (toolTips) {
      tippy(spanAuth[0], {
        content: notifycontent[0],
        theme: 'light',
        interactive: true,
      });  
    }
    
    ulauthors.append(liauth)
  }
  journaldiv = $("<div/>").appendTo(art)
  if ("container-title-short" in publi) {
    var title_short = $("<span/>").text(publi["container-title-short"])
    journaldiv.append(title_short)
    if (toolTips) {
      tippy(title_short[0], {
        content: publi["container-title"],
        theme: 'light',
      });
    }
  }
  else {
    $("<span/>").text(publi["container-title"]).appendTo(journaldiv)
  }
  var datArr = publi.issued["date-parts"][0]
  var date = new Date(datArr[0], datArr[1] - 1, datArr[2])
  journaldiv.append(" ")
  $("<span/>").text(date.getFullYear().toString()).appendTo(journaldiv)
  journaldiv.append(" ")
  $("<span/>").text(publi.volume).appendTo(journaldiv)
  if (publi.issue) {
    $("<span/>").addClass("issue").text(publi.issue).appendTo(journaldiv)
    journaldiv.append(", ")
    $("<span/>").text(publi.page).appendTo(journaldiv)
  }
  $("<a/>", {
    href: publi.URL,
    target: "_blank"
  }).text(String.raw`DOI: ${publi.DOI}`).appendTo(art)
  $("<p/>").append("Published on ").append($("<time/>", {
    datetime: JSON.stringify(date)
  }).text(date.toLocaleDateString("en-us", {
    day: "numeric",
    month: "short",
    year: "numeric"
  }))).appendTo(art)
  return art
}