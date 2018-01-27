function rgbToHex(rgb) {
    return rgb.match(/\d+/g).map(
        num => ('0' + parseInt(num, 10).toString(16)).slice(-2)
    ).join('');
}

var all = [];
document.querySelectorAll('.IssueLabel').forEach(function (node) {
    all.push(
        rgbToHex(node.style.backgroundColor) + ',' +
        rgbToHex(node.style.color)
    );
});

var textarea = document.createElement('textarea');
textarea.innerHTML = all.join('\n');
document.body.appendChild(textarea);
