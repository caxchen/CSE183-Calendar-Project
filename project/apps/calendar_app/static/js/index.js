let app = {}


function main() {

    document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth' //dayGridDay
        });

        /*calendar.addEvent({
            id: 'test1',
            title: 'test event',
            start: '2023-06-03T14:30:00'
        })*/
        calendar.render();

        axios.get("../get_events").then(function(r) {
            if (r.data.events) {
                for (let i=0; i<r.data.events.length; i++) {
                    let name = r.data.events[i].name;
                    let time = r.data.events[i].event_time;
                    let description = r.data.events[i].description;
                    calendar.addEvent({
                        //id: 'test1',
                        title: name,
                        start: time,
                        extendedProps: {
                            description: description
                        }
                    })
                }
            }
        });
    });
    console.log("called main!", Math.random());
}

main();