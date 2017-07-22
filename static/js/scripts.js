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
    var boxHeight = linkQuanity * 33 + linkQuanity * 2;
    var count = 0;
    link.onclick = function() {
        count += 1;
        if (count % 2 === 1) {
            list.style.height = boxHeight - 4 + "px";
        } else {
            list.style.height = "0";
        };
    };
};

function userBoxColor() {
    var boxes = document.getElementsByClassName('user-box');
    var colors = [{color:'#3498db', shadow:'#1468a1'},
                  {color:'#9b59b6', shadow:'#613474'},
                  {color:'#34495e', shadow:'#1b2b3c'},
                  {color:'#f1c40f', shadow:'#9e8006'},
                  {color:'#e57e22', shadow:'#935015'},
                  {color:'#e74c3c', shadow:'#912a1f'},
                  {color:'#bdc3c7', shadow:'#72777a'},
                  {color:'#2ecc71', shadow:'#16713d'},
                  {color:'#16a085', shadow:'#0d6756'},
                  {color:'#e91e63', shadow:'#87123a'},
                  {color:'#8bc34a', shadow:'#4f7326'},
                  {color:'#673ab7', shadow:'#381b6b'},
                  {color:'#00bcd4', shadow:'#026c79'},
                  {color:'#795548', shadow:'#462f27'},
                  {color:'#607d8b', shadow:'#3b4e58'},
    ]
    var shadowGen = function(color, slen) {
        shadow = ''
        for (let i = 1; i < slen; i++) {
            shadow += i + 'px ' + i + 'px ' + color;
            if (i !== slen - 1) {
                shadow += ', '
            };
        };
        return shadow;
    };

    for (let i = 0; i < boxes.length; i++) {
        var idx = Math.floor(Math.random() * colors.length)
        boxes[i].style.background = colors[idx].color;
        boxes[i].childNodes[3].style.textShadow = shadowGen(colors[idx].shadow, 7);
    };
};

function blurLetter() {
    var boxes = document.getElementsByClassName('user-box');
    for (let i = 0; i < boxes.length; i++) {
        boxes[i].onmouseover = function() {
            this.firstElementChild.style.background = "rgba(40, 40, 40, 0.30)";
            this.childNodes[3].style.filter = "blur(8px)";
            this.getElementsByClassName('user-details')[0].style.opacity = '1';
        }
        boxes[i].onmouseout = function() {
            this.firstElementChild.style.background = "initial";
            this.childNodes[3].style.filter = "initial";
            this.getElementsByClassName('user-details')[0].style.opacity = '0';
        };
    };
};

function shrinkName() {
    var userlinks = document.getElementsByClassName('userlink');
    for (let i = 0; i < userlinks.length; i++) {
        if (userlinks[i].innerHTML.length > 10) {
            userlinks[i].style.fontSize = (-1.8 * userlinks[i].innerHTML.length + 46) + "px";
        };
    };
};

function dismissFlash() {
    if (document.getElementById('fm-container')) {
        var closebtns = document.getElementsByClassName('close-flash-btn')
        var container = document.getElementById('fm-container')
        for (let i = 0; i < closebtns.length; i++) {
            closebtns[i].onclick = function () {
                closebtns[i].parentElement.style.display = "none";
            };
        };
    };
};

///// REAL TIME FORM VALIDATION /////

function validateInput(input) {
    var errors = [];
    if (input.value === "") {
        errors.push("You cannot leave this field blank.");
    } else {
        if (input.value.length > 20) {
            errors.push("Your username needs to be shorter than 20 characters.");
        } else if (input.value.length < 3) {
            errors.push("Your username needs to be at least 3 characters long.");
        } else if (!input.value.charAt(0).match(/^[a-zA-Z]+$/))
            errors.push("Your username must start with a letter.")
    };

    return errors
};

function errorMessaging() {
    var inputFields = document.getElementsByClassName('signup-field');
    for (let i = 0; i < inputFields.length; i++) {
        inputFields[i].onclick = function() {
            var errorMsgs = this.nextElementSibling;
            errorMsgs.style.display = 'none';
            this.className = this.className.replace(new RegExp('(?:^|\\s)'+ 'error-border' + '(?:\\s|$)'), '');
        };
        inputFields[i].onblur = validateInput(this);
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

addLoadEvent(userBoxColor)
addLoadEvent(blurLetter);
addLoadEvent(charCounter);
addLoadEvent(expandList);
addLoadEvent(shrinkName);
addLoadEvent(dismissFlash);
addLoadEvent(checkInput);
