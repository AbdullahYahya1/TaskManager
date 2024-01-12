async function sendNumber(number,task_type) {
    try {
        const response = await fetch('send_number/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ number: number , task_type: task_type})
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
        item.addEventListener('click', function() {
            this.classList.toggle('strikethrough');
            sendNumber(this.classList[0] , this.classList[1]);
        });
    });




    let addbutton = document.querySelectorAll('.addbutton');
    let addContainer = document.querySelector('.addContainer');
    addbutton.forEach(button => {
        button.addEventListener('click',()=>{
            addContainer.classList.toggle('view');
        })  
    });


});
