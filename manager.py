import server
import streamer
import threading



print "Starting COMSC Twitter streamer web server..."
t2 = threading.Thread(target = server.start_server)
t2.daemon = True
t2.start()

print "Starting COMSC Twitter streamer Tweet-stream..."
t1 = threading.Thread(target = streamer.start_streamer)
t1.daemon = True
t1.start()

print "\nPress ctrl-C to exit\n"

# Run indefinitely or until cancelled:
while True:
    pass
