
function mobileMenuOpen() {


    let sideElm = document.getElementById("side-wrapper");

    // console.log(sideElm);

    sideElm.style.width = "100%";
    sideElm.style.display = "block";
    sideElm.classList.add('opened');
}

function mobileMenuClose() {

    let sideElm = document.getElementById("side-wrapper");

    if (sideElm.classList.contains('opened')) {
        sideElm.style.display = "none";
    }
}


function attachTocMouseEventListener() {

    const sideBarUls = Array.from(document.getElementById("toc-details").getElementsByTagName("ul"));

    sideBarUls.forEach((elm, idx) => {
        if (idx > 0) {
            elm.addEventListener('mouseover', function(e) {
                elm.previousSibling.style.color = "#FAB57F";
            });
            elm.addEventListener('mouseout', function(e) {
                elm.previousSibling.style.color = "lightgrey";
            });
        }
    });
}


let tocNodes = document.getElementById("toc-details").children

Array.from(tocNodes).forEach(node => {
    if (node.nodeName.toLowerCase() == 'ul') {
        node.addEventListener("click", mobileMenuClose);
    }
})
attachTocMouseEventListener();
