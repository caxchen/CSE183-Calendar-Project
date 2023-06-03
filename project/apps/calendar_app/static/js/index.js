let app = {}


function main() {

    document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth', //dayGridDay
          eventClick: function(info) {
            window.location.href =`../view_event/${info.event.id}`;
          }
          
        });
        
        calendar.render();

        axios.get("../get_events").then(function(r) {
            if (r.data.events) {
                for (let i=0; i<r.data.events.length; i++) {
                    let event_id = r.data.events[i].id;
                    let name = r.data.events[i].name;
                    let time = r.data.events[i].event_time;
                    let description = r.data.events[i].description;
                    calendar.addEvent({
                        id: event_id,
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
}

main();