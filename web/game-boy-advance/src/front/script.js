
function getApiURL(endpoint) {
    return "/api" + endpoint;
}

// Checking JWT expiration
function isValid(token) {
    try {
        const decoded = jwt_decode(token);
        const currentTime = Math.floor(Date.now() / 1000);

        if (!decoded.exp) {
            return false;  
        }

        return decoded.exp > currentTime;
        
    } catch (error) {
        console.error('Invalid token:', error);
        return false; 
    }
}

// JWT Management 
function getPage() {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    if (accessToken) {
        const validity = isValid(accessToken);
        if (validity) {
            return;
        } else {
            if (isValid(refreshToken)) {
                fetch(getApiURL('/refresh'), {
                    method: 'GET',
                    headers: {
                        'X-Access-Token': refreshToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data && data.access_token && data.refresh_token) {
                        localStorage.setItem('access_token', data.access_token);
                        localStorage.setItem('refresh_token', data.refresh_token);
                        getPage(); 
                    } else {
                        console.error("Failed to refresh token. Redirecting to login...");
                        return redirectToLogin();
                    }
                })
                .catch(error => {
                    console.error("Error refreshing token:", error);
                    return redirectToLogin();
                });
            } else {
                return redirectToLogin();
            }
        }
    } else {
        return redirectToLogin();
    }
}

function redirectToLogin() {
    window.location.href = '/login.html';
}


// Register
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('register-username').value;
        const mail = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const notif_div=document.querySelector('.notif')

        fetch(getApiURL('/register'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, mail, password }),
        })
        .then(response => response.json())
        .then(data => {
            notif_div.style.display='block';
            const notif = document.getElementById('notif-register');
            if (data.message) {
                notif.textContent = data.message;
                notif.style.color = 'green';
                setTimeout(() => {
                    window.location.href = '/login.html'; 
                }, 1000);
            } else if (data.error) {
                notif.textContent = data.error;
                notif.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const notif = document.getElementById('notif-register');
            notif.textContent = 'An error occurred';
            notif.style.color = 'red';
        });
    });
}

// Login
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const notif_div = document.querySelector('.notif');
        
        fetch(getApiURL('/login'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            notif_div.style.display = 'block';
            const notif = document.getElementById('notif-login');
            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                if (data.refresh_token) {
                    localStorage.setItem('refresh_token', data.refresh_token);
                }
                notif.textContent = "Logging In ... ";
                setTimeout(() => {
                    window.location.href = "/home.html";
                }, 1000);
            } else if (data.error) {
                notif.textContent = data.error;
                notif.style.color = 'red';
            }
        })
        .catch(error => {
            const notif = document.getElementById('notif-login');
            notif.textContent = 'An error occurred';
            notif.style.color = 'red';
        });
    });
}




// Logout
const logoutLink = document.getElementById('logout-link');
if (logoutLink) {
    const notif = document.getElementById('general-notif');

    logoutLink.addEventListener('click',  function(event) {
        event.preventDefault();

        getPage();

        const url = getApiURL('/logout');

        // Logout refresh token
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken){
        fetch(url, {
            method: 'GET',
            headers: {
                'X-Access-Token': refreshToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                localStorage.removeItem('refresh_token');
            } else {
                notif.textContent = 'Unexpected response format.';
                notif.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', 'Data error');
        });
        }

        // Logout access token
        const accessToken = localStorage.getItem('access_token');
        fetch(url, {
            method: 'GET',
            headers: {
                'X-Access-Token': accessToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                localStorage.removeItem('access_token');
                notif.textContent = "Logging out";
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 1000);
            } else {
                notif.textContent = 'Unexpected response format.';
                notif.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', 'Data error');
        });
});
}



// Create Post
const postForm = document.getElementById('post-form');
if (postForm) {
    postForm.addEventListener('submit', function(event) {
        event.preventDefault();

        getPage();

        const title = document.getElementById('title').value;
        const content = document.getElementById('content-form').value;
        const isPrivate = document.getElementById('is_private').checked;
        const accessToken = localStorage.getItem('access_token');

        fetch(getApiURL('/post/write'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Access-Token': accessToken 
            },
            body: JSON.stringify({
                title: title,
                content: content,
                is_private: isPrivate
            })
        })
        .then(response => response.json())
        .then(data => {
            const notif = document.getElementById('notif-post');
            if (data.message) {
                notif.textContent = 'Post created successfully';
                notif.style.color = 'aqua';
            } else {
                notif.textContent = data.error;
                notif.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', 'Data error');
        });
    });
}

// Displaying User's posts (public and private)
const usersLink = document.getElementById('posts-link');
if (usersLink) {
    usersLink.addEventListener('click',  function(event) {
        event.preventDefault();

        getPage();

        const accessToken = localStorage.getItem('access_token');
        const decoded = jwt_decode(accessToken);
        const url = getApiURL('/user/'+decoded.sub);

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Access-Token': accessToken
            }
        })
        .then(response => response.json())

        .then(data => {
            if (data.error){
                const notif = document.getElementById('general-notif');
                notif.textContent=data.error;
            }
            else {
                const contentSections = document.querySelectorAll('#content > div');
                contentSections.forEach(section => {
                    section.style.display = 'none';
                });

                const contentContainer = document.getElementById('posts-container');
                contentContainer.innerHTML = '';
                if (data.posts){
                    data.posts.forEach(post => {
                        const postDiv = document.createElement('div');
                        postDiv.classList.add('post'); 

                        const titleElement = document.createElement('h3');
                        titleElement.textContent = post.title || 'Untitled'; 
                        postDiv.appendChild(titleElement);

                        if (post.is_private){
                            const space = document.createTextNode(' ');
                            titleElement.appendChild(space);

                            const privateElement = document.createElement('i');
                            privateElement.classList.add('fa'); 
                            privateElement.classList.add('fa-lock');
                            titleElement.appendChild(privateElement);
                        };

                        const contentElement = document.createElement('p');
                        contentElement.textContent = post.content || 'No content available'; 
                        postDiv.appendChild(contentElement);

                        contentContainer.appendChild(postDiv);
                    });
                }
                else{

                    // Show message if there are no posts
                    const message = document.createElement('p');
                    message.textContent = 'No posts yet.';
                    contentContainer.appendChild(message);
                }
                ;

                document.getElementById('user-posts-container').style.display = 'flex';
                
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    
});
}


// Displaying the list of all users 
const allusersLink = document.getElementById('users-link');
if (allusersLink) {
    allusersLink.addEventListener('click', function(event) {
        event.preventDefault();

        getPage();

        const accessToken = localStorage.getItem('access_token');
        const url = getApiURL('/users');

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Access-Token': accessToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                const notif = document.getElementById('general-notif');
                notif.textContent = data.error;
            } else {
                const contentSections = document.querySelectorAll('#content > div');
                contentSections.forEach(section => {
                    section.style.display = 'none';
                });
            
                console.log(data);
            
                // Show the user details section
                const userDetails = document.getElementById('user-details');
                userDetails.style.display = 'flex';
            
                // Clear previous table rows if any
                const userTableBody = document.querySelector('#user-table tbody');
                userTableBody.innerHTML = '';
            
                // Populate the table with users
                data.forEach(user => {
                    const row = document.createElement('tr');
            
                    const usernameCell = document.createElement('td');
                    usernameCell.textContent = user.username;
                    row.appendChild(usernameCell);
            
                    const emailCell = document.createElement('td');
                    emailCell.textContent = user.mail;
                    row.appendChild(emailCell);
            
                    userTableBody.appendChild(row);
                });
            }            
            
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}



// Feed : Displaying All Public Posts of all users
const feedLink = document.getElementById('feed-link');
if (feedLink) {
    feedLink.addEventListener('click', function(event) {
        event.preventDefault();

        getPage();

        const accessToken = localStorage.getItem('access_token');
        const url = getApiURL('/feed');

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Access-Token': accessToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                const notif = document.getElementById('general-notif');
                notif.textContent = data.error;
            } else {
                const contentSections = document.querySelectorAll('#content > div');
                contentSections.forEach(section => {
                    section.style.display = 'none';
                });

                const contentContainer = document.getElementById('posts-container');
                contentContainer.innerHTML = '';

                data.forEach(post => {
                    const postDiv = document.createElement('div');
                    postDiv.classList.add('post');

                    const titleElement = document.createElement('h3');
                    titleElement.textContent = post.title || 'Untitled';
                    postDiv.appendChild(titleElement);

                    const breakElement = document.createElement('br');
                    postDiv.appendChild(breakElement);
                    postDiv.appendChild(breakElement);

                    const dateElement = document.createElement('p');
                    dateElement.classList.add('creation-date'); 
                    dateElement.textContent = post.creation_date ? `Created on: ${new Date(post.creation_date).toLocaleDateString()}` : 'No creation date';
                    postDiv.appendChild(dateElement);

                    postDiv.appendChild(breakElement);
                    postDiv.appendChild(breakElement);

                    const contentElement = document.createElement('p');
                    contentElement.textContent = post.content || 'No content available';
                    postDiv.appendChild(contentElement);

                    contentContainer.appendChild(postDiv);
                });

                document.getElementById('user-posts-container').style.display = 'flex';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}
