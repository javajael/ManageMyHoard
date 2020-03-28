"use strict";

$("#show-projects").on('submit',(evt) => {
    evt.preventDefault();
    const projDiv = $('#show-projects');
    
    $.get('/in_progress_projects.json', (res) => {
        projectDiv.append(`<tr>`);
        projectDiv.append(`<th>Project Name</th>`);
        projectDiv.append(`<th>Status</th>`);
        projectDiv.append(`<th>Description</th>`);
        projectDiv.append(`</tr>`);

        for (project of res) {
            projDiv.append(`<tr>`);
            projDiv.append(`<td>${ project.name }</td>`);
            projDiv.append(`<td>${ project.status }</td>`);
            projDiv.append(`<td>${ project.description }</td>`);
            projDiv.append(`</tr>`);            
        }
    });

});
/*$("#show-projects").onclick('submit', showProjects);
$('#get-human').on('submit', (evt) => {
        evt.preventDefault();
        const selectedId = $('#human-id').val();
        alert(selectedId);
      });*/

