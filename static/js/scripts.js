document.addEventListener('DOMContentLoaded', function () {
    let deleteForm = null;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmationModal'));
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');

    function showDeleteModal(event, taskId) {
        event.preventDefault();
        deleteForm = event.target;
        deleteModal.show();
    }

    confirmDeleteButton.addEventListener('click', function () {
        if (deleteForm) {
            deleteForm.submit();
        }
    });

    function showTaskDetails(taskId) {
        console.log('Showing details for task ID:', taskId); // Debug statement
        fetch(`/task-details/${taskId}`)
            .then(response => response.json())
            .then(data => {
                console.log('Task details fetched:', data); // Debug statement
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('taskTitle').innerText = data.title;
                    document.getElementById('taskDescription').innerText = data.description;
                    document.getElementById('taskCategory').innerText = data.category;
                    document.getElementById('taskPriority').innerText = data.priority;

                    // Show the modal
                    const taskDetailsModal = new bootstrap.Modal(document.getElementById('taskDetailsModal'));
                    taskDetailsModal.show();
                }
            })
            .catch(error => console.error('Error fetching task details:', error));
    }

    function toggleTaskCompletion(taskId) {
        const checkbox = document.getElementById(`complete-${taskId}`);
        fetch(`/toggle-task-completion/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ form.csrf_token._value() }}'
            }
        }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    const cardTitle = checkbox.closest('.card-body').querySelector('.card-title');
                    if (checkbox.checked) {
                        cardTitle.classList.add('text-decoration-line-through');
                    } else {
                        cardTitle.classList.remove('text-decoration-line-through');
                    }
                }
            })
            .catch(error => console.error('Error toggling task completion:', error));
    }

    window.showDeleteModal = showDeleteModal;
    window.showTaskDetails = showTaskDetails;
    window.toggleTaskCompletion = toggleTaskCompletion;
});

