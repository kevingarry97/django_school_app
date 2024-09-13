document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sendAjaxRequest(url, method, data, successCallback, errorCallback) {
        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => successCallback(data))
        .catch(error => errorCallback(error));
    }

    // Add event listeners for CRUD operations
    document.body.addEventListener('click', function(event) {
        if (event.target.classList.contains('ajax-create')) {
            event.preventDefault();
            const form = event.target.closest('form');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            sendAjaxRequest(form.action, 'POST', data, 
                function(response) {
                    // Handle successful creation
                    console.log('Created successfully:', response);
                    // Refresh the list or add the new item to the DOM
                },
                function(error) {
                    console.error('Error creating:', error);
                }
            );
        }
        else if (event.target.classList.contains('ajax-update')) {
            event.preventDefault();
            const form = event.target.closest('form');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            sendAjaxRequest(form.action, 'PUT', data, 
                function(response) {
                    // Handle successful update
                    console.log('Updated successfully:', response);
                    // Update the item in the DOM
                },
                function(error) {
                    console.error('Error updating:', error);
                }
            );
        }
        else if (event.target.classList.contains('ajax-delete')) {
            event.preventDefault();
            const url = event.target.href;
            
            sendAjaxRequest(url, 'DELETE', {}, 
                function(response) {
                    // Handle successful deletion
                    console.log('Deleted successfully:', response);
                    // Remove the item from the DOM
                },
                function(error) {
                    console.error('Error deleting:', error);
                }
            );
        }
    });
});