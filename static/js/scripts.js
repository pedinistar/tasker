let deleteForm = null;

function showDeleteModal(event, taskId) {
        event.preventDefault(); // Prevent the default form submission
        deleteForm = event.target; // Save the form that will be submitted

        const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmationModal'));
        deleteModal.show();

        // Add click event listener to the confirm delete button
        document.getElementById('confirmDeleteButton').addEventListener('click', function () {
            if (deleteForm) {
                deleteForm.submit(); // Submit the form
            }
        });
}

function showTaskDetails(taskId) {
        fetch(`/task-details/${taskId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Populate the modal with task details
                    document.getElementById('taskTitle').innerText = data.title;
                    document.getElementById('taskDescription').innerText = data.description;
                    document.getElementById('taskCategory').innerText = data.category;
                    document.getElementById('taskPriority').innerText = data.priority;
                    document.getElementById('taskDeadline').innerText = data.deadline;

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
                    // Update the task appearance based on the completion status
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