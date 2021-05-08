#include <stdio.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>

// that's how an evdev event is structured
//struct input_event {
//        struct timeval time;
//        unsigned short type;
//        unsigned short code;
//        unsigned int value;
//};

int main(int argc, char* argv[]) 
{
    // path to the input device (e.g. /dev/input/event1)
    char* event_handle = argv[1];

    // open the input device so we can read events
    int input_fd = open(event_handle, O_RDONLY | O_NONBLOCK);

    if(!input_fd)
    {
        // something went wrong -> exit
        printf("could not open input device");
        return 1;
    }

    struct input_event inputEvent;
    int err = -1;

    while(1)
    {
        // read form input device and store it in inputEvent; returns -1 if unsuccessful (e.g. because there are no events)
        err = read(input_fd, &inputEvent, sizeof(struct input_event));

        if(err != -1)
        {
            // print the input event
            printf("%d %d %d\n", inputEvent.type, inputEvent.code, inputEvent.value);
        }
    }

    return 0;
}
