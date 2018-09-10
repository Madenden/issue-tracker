let endpoint = '/chart/data/';
let labels = [];
let tickets_qty = [];
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data) {
        labels = data.labels;
        tickets_qty = data.tickets_qty;
        let ctx = document.getElementById('myChart').getContext('2d');
        let myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: '# of Votes',
                    data: tickets_qty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderColor: [
                        'rgba(255,255,255,1)'
                    ]
                }]
            }
        });
    },
    error: function(error_data) {
        console.log("error");
        console.log(error_data);
    }
});