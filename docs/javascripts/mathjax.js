// MathJax configuration for the formulas in the synced wiki pages, which use
// $...$ and $$...$$ as GitHub does. pymdownx.arithmatex (generic mode) wraps
// them in \(...\) and \[...\] for MathJax to typeset.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

// Instant navigation swaps pages without a reload, so typeset each new page.
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
