
document.querySelector("#read-button").addEventListener('click', function() {
    let file = document.querySelector("#file-input").files[0];
    let reader = new FileReader();
    reader.addEventListener('load', function(e) {
        let text = e.target.result;
        doChart(JSON.parse(text));
    });
    reader.readAsText(file);
})

function doChart(datasets) {
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: ['Letter 1', 'Letter 2', 'Letter 3', 'Letter 4', 
                'Chapter 1',
                'Chapter 2',
                'Chapter 3',
                'Chapter 4',
                'Chapter 5',
                'Chapter 6',
                'Chapter 7',
                'Chapter 8',
                'Chapter 9',
                'Chapter 10',
                'Chapter 11',
                'Chapter 12',
                'Chapter 13',
                'Chapter 14',
                'Chapter 15',
                'Chapter 16',
                'Chapter 17',
                'Chapter 18',
                'Chapter 19',
                'Chapter 20',
                'Chapter 21',
                'Chapter 22',
                'Chapter 23',
                'Chapter 24',
            ],
            datasets: datasets
        },

        // Configuration options go here
        options: {}
    });
}