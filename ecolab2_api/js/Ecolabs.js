let divCell=document.querySelector("#lesCell")


async function fetchCell(url){
    try {
    let reponse= await fetch(url)
    let dataCell = await reponse.json()
    return dataCell
    } catch (error) {
        console.error("Erreur lors de la récupération des données des cellules :", error);
    }

}

fetchCell("http://10.119.20.100:8080/").then(function (dataCell){
    for (const cellule of dataCell) {
        console.log(cellule)
       divCell.innerHTML+=afficheCell(cellule)+"<br>"
    }
})

function afficherCell(cellule) {

    return `<p>Nom du pays: ${lePays.name.common}</p>`;
}

