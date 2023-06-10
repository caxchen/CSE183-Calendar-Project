let app = {}



function main() {

    document.addEventListener('DOMContentLoaded', function() {
        // create a calendar
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          // initial view Month
          initialView: 'dayGridMonth',
          // when event clicked, go to view event page
          eventClick: function(info) {
            window.location.href =`../view_event/${info.event.id}`;
          },
          // when day clicked, go to that day
          dateClick: function(info) {
            calendar.changeView('timeGridDay', info.dateStr);
          },
          // custom buttons
          customButtons: {
            testButton1: {
                text: "Month View",
                click: function() {
                    calendar.changeView('dayGridMonth');
                }
            },
            MultiMonthView: {
              text: 'Multiple Month',
              click: function() {
                 calendar.changeView('multiMonthYear')
              }
            }
          },
          // header layout
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,multiMonthYear'
          }
          
        });
        
        // render calendar
        calendar.render();

        // get event data and add to calendar
        axios.get("../get_events").then(function(r) {
            if (r.data.events) {
                for (let i=0; i<r.data.events.length; i++) {
                    let event_id = r.data.events[i].id;
                    let name = r.data.events[i].name;
                    let time = r.data.events[i].event_time;
                    let all_day = r.data.events[i].all_day;
                    let description = r.data.events[i].description;
                    //let color = r.data.categories[r.data.events[i].category - 1].color;
                    if (r.data.events[i].category) {
                      calendar.addEvent({
                        id: event_id,
                        title: name,
                        start: time,
                        allDay: all_day,
                        backgroundColor: r.data.categories[r.data.events[i].category - 1].color,
                        extendedProps: {
                            description: description
                        }
                      });
                    } else {
                      // create calendar event with data from event database
                      calendar.addEvent({
                          id: event_id,
                          title: name,
                          start: time,
                          allDay: all_day,
                          extendedProps: {
                              description: description
                          }
                      });
                    }
                }
                // render calendar
                calendar.render();
            }
        });
    });
}

main();

function back() {
    var calendarEl = document.getElementById('calendar').Calendar;
    console.log(calendarEl);
}