const display = $("#log_display")


const update_log = () => {
    $.ajax({
        type: "GET",
        url: "/log",
        success: function (d){
            display.empty()



            d.forEach(entry => { display.append(`<p>${entry.replace("console.py:10", "")}</p>`)})
        }
    })
}

update_log()
setInterval(update_log, 1000)