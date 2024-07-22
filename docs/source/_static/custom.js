// Suppress package names in autodoc-generated navbar and index TOC
document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll('a.reference.internal');
    links.forEach(function(link) {
        var text = link.textContent;
        var index = text.indexOf('.');
        if (index !== -1) {
            link.textContent = text.substring(index + 1);
        }
    });
});