$(function() {
    let currentTime = "";
    let alarmTime = "";
    
    function time() {
        let time = new Date();
        return time.toLocaleTimeString();
    }
    
    function showTime() {
        currentTime = time();
        return $(".current-time-content").text(time());
    }
    
    showTime();
    setInterval(function() {
        showTime();
        if(alarmTime == currentTime) {
            alert("Wake Up!");
            alarmTime = "";
            $(".alarm-time").hide();
        }
    }, 1000);
    
    $(".alarm-input-btn").click(function(){
        alarmTime = $("#alarm-input").val() + ":00";
        $(".alarm-time").text(`You have alarm at: ${alarmTime}`).show();
    });
    
});