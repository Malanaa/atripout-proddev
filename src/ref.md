Socket Refrence Script.
<script>
        var socket = io();
        let send_message = "Hello from a client"

        socket.emit("send_text_to_server",send_message);
        const message = document.createElement('div');
        const message_p = document.createElement('p')
        message_p.className = 'mt-4 p-2 bg-gray-700 rounded';
        message_p.textContent = send_message;
        message.appendChild(message_p);
        document.body.appendChild(message);

        socket.on('send_text_to_client', function(data){
          const message = document.createElement('div');
          const message_p = document.createElement('p')
          message_p.className = 'mt-4 p-2 bg-gray-700 rounded';
          message_p.textContent = data;

          message.appendChild(message_p);
          document.body.appendChild(message);

        });
</script>