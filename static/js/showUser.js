$(function() {
    const userDiv = $('#user_profile');
    
    $.get('api/user_profile', (res) => {
        for (user of res) {
            console.log(user);
            userDiv.append(`<li>${user.username}</li>`);
            userDiv.append(`<li>${user.email}</li>`);
            userDiv.append(`<div>
                            <p><b>Username:</b> ${user.username}</p>
                            </div>`);
        }
    });

});