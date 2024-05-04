// ==UserScript==
// @name         CartelPy
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  None.
// @author       BOT7420 [3094]
// @match        https://cartelempire.online/*
// @grant        GM_addStyle
// @grant        GM_xmlhttpRequest
// @run-at       document-start
// ==/UserScript==

(async function () {
    "use strict";

    GM_addStyle(`
        input.disabled {
            display: none !important;
        }`);

    handleEnergy();
    const currentURL = window.location.href.toLowerCase();
    if (currentURL.includes("/jobs")) {
        handleJobs();
    } else if (currentURL.includes("/connections")) {
        handleConnections();
    } else if (currentURL.includes("/expedition")) {
        handleExpedition();
    }

    function handleExpedition() {
        const checkElementExist = () => {
            const buttonsNotDisabled = document.querySelectorAll(
                `div.container.expeditionButton div.input-group div.input-group-append input:not(.d-none):not(.disabled):not([style*="display: none"])`
            );
            if (buttonsNotDisabled.length === 0) {
                document.querySelectorAll(`ul#menu li`)[2].querySelector(`a`).querySelector(`span`).innerHTML = "【没有远征】";
            } else {
                document.querySelectorAll(`ul#menu li`)[2].querySelector(`a`).querySelector(`span`).innerHTML = "【" + buttonsNotDisabled.length + "个远征】";
            }

            const selects = document.querySelectorAll(`div.container.expeditionButton div.input-group`);
            if (selects.length > 2) {
                const toHide = document.querySelectorAll(`div.container.expeditionButton div.row.top`);
                var hide_array = [...toHide];
                hide_array.forEach((hide) => {
                    hide.style.display = "none";
                });

                const buttons = document.querySelectorAll(`div.container.expeditionButton div.input-group div.input-group-append input`);
                let buttons_array = [...buttons];
                if (buttons_array.length === 0) {
                    return;
                }
                for (const elem of buttons_array) {
                    const select = elem.parentElement.parentElement.querySelector(`select`);
                    if (select.children.length > 1) {
                        let v = select.children[1].value;
                        elem.value = "【开始】";
                        select.value = v;
                        select.dispatchEvent(new Event("change"));
                        break;
                    }
                }
            }
        };
        let timer = setInterval(checkElementExist, 100);
    }

    function handleEnergy() {
        const checkElementExist = () => {
            const selectedElem = document.querySelector(`span#currentEnergy`);
            if (selectedElem) {
                const home = document.querySelector(`ul#menu li`).querySelector(`a`);
                home.href = "/Connections";
                if (Number(selectedElem.innerHTML) < 20) {
                    home.querySelector(`span`).innerHTML = "【没有能量】";
                } else {
                    home.querySelector(`span`).innerHTML = "【进攻】";
                }
            }
        };
        let timer = setInterval(checkElementExist, 100);
    }

    function handleConnections() {
        const checkElementExist = () => {
            const selectedElem = document.querySelector(`div.card.mb-4 div.card-body tbody`);
            if (selectedElem) {
                clearInterval(timer);
                let activeCount = 0;

                const tr = selectedElem.querySelectorAll(`tr`);
                var tr_array = [...tr];
                tr_array.forEach((tr) => {
                    if (!tr.querySelector(`td`).innerHTML.includes("Active")) {
                        tr.style.display = "none";
                    } else {
                        activeCount += 1;
                        const url = tr.querySelector(`a`).href;
                        tr.querySelector(`td`).style.backgroundColor = "#AA0000";
                        tr.querySelector(`td`).innerHTML = "【Active】";
                        tr.querySelector(`td`).addEventListener(
                            "click",
                            function (event) {
                                window.location = url;
                            },
                            false
                        );
                    }
                });
                if (activeCount === 0) {
                    document.querySelectorAll(`ul#menu li`)[1].querySelector(`a`).querySelector(`span`).innerHTML = "【没有目标】";
                }
            }
        };
        let timer = setInterval(checkElementExist, 100);
    }

    function handleJobs() {
        const checkElementExist = () => {
            const selectedElem = document.querySelector(`img.img-fluid.img-thumbnail.mb-2`);
            if (selectedElem) {
                clearInterval(timer);
                const divs = document.querySelectorAll(`div.col-6`);
                var div_array = [...divs];
                div_array.forEach((div) => {
                    if (!div.querySelector(`h5`)?.innerHTML.includes("Arson")) {
                        div.style.display = "none";
                    }
                    // Array.from(div.firstChild.firstChild.children).forEach((elem) => {
                    //     if (elem.tagName.toLowerCase() !== "h5" && elem.tagName.toLowerCase() !== "form") {
                    //         elem.style.display = "none";
                    //     }
                    // });
                });
            }
        };
        let timer = setInterval(checkElementExist, 100);
    }
})();
