const updatesDropDown = document.getElementsByClassName('updates-dropdown')
const dropContainer = document.getElementsByClassName('drop-wrapper')

function Drop(updatesDropDown, dropContainer) {
    if (updatesDropDown.style.display == "none" && dropContainer.style.display == "none") {
        updatesDropDown.style.display == "block";
        dropContainer.style.display == "block";
    } else {
        updatesDropDown.style.display == "none";
        dropContainer.style.display == "block"; 
    }
}