
let btnAdd = document.querySelector('svg');
let table = document.querySelector('table');


let nameInput = document.querySelector('#name');
let ageInput = document.querySelector('#age');
let countryInput = document.querySelector('#country');


btnAdd.addEventListener('click', () => {
    let name = nameInput.value;
    let age = ageInput.value;
    let country = countryInput.value;

    let template = `
                <tr>
                    <td>${name}</td>
                    <td>${age}</td>
                    <td>${country}</td>
                </tr>`;

    table.innerHTML += template;
});