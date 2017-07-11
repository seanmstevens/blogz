// Newpost Character Counter

function charCounter() {
    if (window.location.pathname == "/newpost") {
        var text = document.getElementById('textarea');
        var counter = document.getElementById('counter');

        document.getElementById('counter').innerHTML = (500 - text.value.length);

        function count() {
            counter.innerHTML = (500 - this.value.length);
            if (this.value.length >= 450) {
                counter.style.color = "#f44336";
            } else {
                counter.style.color = "#3f3f43";
            };
        };

        text.addEventListener('keyup', count);
        text.addEventListener('keydown', count);
    };
};

// Expanding Sidenav

function openNav() {
    var sidenav = document.getElementById('sidenav');
    var main = document.getElementById('main');
    var footer = document.getElementById('menu-footer');
    sidenav.style.transform = "translate(0)";
    sidenav.style.borderRightWidth = "5px";
    footer.style.transform = "translate(0)";
    main.style.transform = "translate(85px)";
    document.getElementById('overlay').className += ' overlay-show';
}

function closeNav() {
    var sidenav = document.getElementById('sidenav');
    var main = document.getElementById('main');
    var footer = document.getElementById('menu-footer');
    sidenav.style.transform = "translate(-100%)";
    sidenav.style.borderRightWidth = "0";
    footer.style.transform = "translate(-100%)";
    main.style.transform = "translate(0)";
    document.getElementById('overlay').className = 'overlay';
};

// Expanding Submenu

function expandList() {
    var list = document.getElementById('expanding-list');
    var link = document.getElementById('entries-link');
    var linkQuanity = document.querySelectorAll('#expanding-list .side-navlink').length;
    var boxHeight = linkQuanity * 33;
    var count = 0;
    link.onclick = function() {
        count += 1;
        if (count % 2 === 1) {
            list.style.height = boxHeight + "px";
        } else {
            list.style.height = "0";
        };
    };
};

function randomColor() {
    var boxes = document.getElementsByClassName('user-box');
    var colors = ['#3498db',
                  '#9b59b6',
                  '#34495e',
                  '#f1c40f',
                  '#e57e22',
                  '#e74c3c',
                  '#bdc3c7',
                  '#2ecc71',
                  '#16a085',           
    ]
    for (var i = 0; i < boxes.length; i++) {
        boxes[i].style.background = colors[Math.floor(Math.random() * colors.length)]
    };
};

function blurLetter() {
    var boxes = document.getElementsByClassName('user-box');
    for (var i = 0; i < boxes.length; i++) {
        boxes[i].onmouseover = function() {
            this.firstElementChild.style.background = "rgba(40, 40, 40, 0.55)";
            this.firstElementChild.firstElementChild.style.filter = "blur(8px)";
        }
        boxes[i].onmouseout = function() {
            this.firstElementChild.style.background = "initial";
            this.firstElementChild.firstElementChild.style.filter = "initial";
        };
    };
};

function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            if (oldonload) {
                oldonload();
            }
        func();
        };
    };
};

addLoadEvent(randomColor)
addLoadEvent(blurLetter);
addLoadEvent(charCounter);
addLoadEvent(expandList);
