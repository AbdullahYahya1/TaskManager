async function sendNumber(number, task_type) {
    try {
        const response = await fetch('send_number/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ number: number, task_type: task_type })
        });
        const data = await response.json();
        console.log('Response from Django:', data);
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    let taskItems = document.querySelectorAll('.item');
    taskItems.forEach(function(item) {
        item.addEventListener('click', function(event) {
            // Check if the clicked element is not the "Details" button
            if (!event.target.matches('.details-button')) {
                this.classList.toggle('strikethrough');
                sendNumber(this.classList[0], this.classList[1]);
            }
        });
    });

    let addbutton = document.querySelectorAll('.addbutton');
    let addContainer = document.querySelector('.addContainer');
    addbutton.forEach(button => {
        button.addEventListener('click', () => {
            addContainer.classList.toggle('view');
        });
    });

    // Handle the click event for "Details" buttons
    let detailButtons = document.querySelectorAll('.details-button');
    detailButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();
        });
    });

    window.onload = function() {
        var roomSelect = document.getElementById('roomSelect');
        var currentRoomId = new URLSearchParams(window.location.search).get('room_id');
        for (var i = 0; i < roomSelect.options.length; i++) {
            if (roomSelect.options[i].value.includes('room_id=' + currentRoomId)) {
                roomSelect.selectedIndex = i;
                break;
            }
        }
    };
    document.getElementById('roomSelect').addEventListener('change', function() {
        window.location.href = this.value;
    });
});
