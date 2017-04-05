<!DOCTYPE html>
<html>
<?php require('header.php'); ?>
  <body>
 <div class="container">
      <div class="header clearfix">
        <nav>
          <ul class="nav nav-pills pull-right">
            <li role="presentation" class="active"><a href="#">Home</a></li>
            <li role="presentation"><a href="about.php">About</a></li>
            <li role="presentation"><a href="contact.php">Contact</a></li>
          </ul>
        </nav>
        <h3 class="text-muted">Voice</h3>
      </div>

      <div class="jumbotron" id="boxy-content">
		<h2>Nagrywanie mowy</h2>
		
		<form id="recording-form" name="recording-form" action="nagraj.php" method="post" autocomplete="on" onsubmit="return false;">  <!--Formularz-->
		<div class="form-group">
			<label for = "imie">Imię i Nazwisko: </label>
			<input type="text" name="imie" id="imie" required />
		</div>
		<div class="form-group">
		<label for ="option-list">Komenda</label>
		<select name="option-list" id="option-list">
			<option selected="selected">Bieg</option>
			<option>Brzuszki</option>
			<option>Chód</option>
			<option>Posiłek</option>
			<option>Komputer</option>
			<option>Leżenie</option>
			<option>Pisanie</option>
			<option>Przysiady</option>
			<option>Siedzenie</option>
			<option>Stanie</option>
			<option>Upadek</option>
			<option>Tak</option>
			<option>Nie</option>
		</select>
		</div>
		<?php
			$dzis=getdate();
			$dzien=$dzis['mday'];
			$miesiac=$dzis['mon'];
			$rok=$dzis['year'];
			$godz=$dzis['hours'];
			$min=$dzis['minutes'];
			$sek=$dzis['seconds'];
		?>
			<input class="btn btn-success" type="submit" onclick="getDataAndChangeToRecording()" value="Rozpocznij nagrywanie" />
			<input class="btn btn-warning" type="reset" value="Wyczyść dane" />
		</form>
		</div>

      <footer class="footer">
        <p>&copy; 2017 Akademia Górniczo-Hutnicza</p>
      </footer>
    </div> <!-- /container -->

	
	<script>
    var ua = navigator.userAgent.toLowerCase();
    var isAndroid = ua.indexOf("android") > -1; //&& ua.indexOf("mobile");
    if(isAndroid) {
        document.getElementById("container").style.width = "100%"
    }
    
    var selectedOption;
    var name;
    
    function getDataAndChangeToRecording(){
        var nameField = document.getElementById("imie");
        name = nameField.value;
        ilosc = 0;
        var optionList = document.getElementById("option-list");
        selectedOption = optionList.options[optionList.selectedIndex].text;
        var recordDiv = document.getElementById("boxy-content");
        recordDiv.innerHTML = '<h2>Nagrywanie mowy</h2>\
            <h3> Jako: ' + name + '</h3>\
            <h3> Czynność: ' + selectedOption + '<h3>\
			<div class="row">\
			<audio id="audio" controls></audio><br>\
			</div>\
			<div class="row">\
				<div class="col-xs-12 col-md-6">\
					<button class="btn btn-success btn-lg" id="record" disabled > Rozpocznij nagranie</button>\
				</div>\
				<div class="col-xs-12 col-md-6">\
					<button type="button" class="btn btn-primary btn-lg " onclick="location.reload()" > Wybierz inną czynność</button>\
				</div>\
			</div>\
            <h3 id="liczbaNagran"> Liczba nagrań: ' + ilosc + '<h3>';
			//<a id="downloadLink" href></a>';
			
        // nagrywanie
        var recordButton, stopButton, recorder;
        var chunks = [];
        var timeLimit;
        var downloadLink = document.querySelector('a#downloadLink');
            recordButton = document.getElementById("record");
            //stopButton = document.getElementById("stop");
            navigator.mediaDevices.getUserMedia({
                audio: true
            })
                .then(function (stream) {

                    recordButton.disabled = false;
                    recordButton.style.backgroundColor = "##5cb85c";
                    recordButton.addEventListener('click', startRecording);
                    //stopButton.addEventListener('click', stopRecording);
                    recorder = new MediaRecorder(stream);
                    recorder.ondataavailable = uploadAudio
                });

        function startRecording() {
            chunks = [];
            recordButton.removeEventListener('click', startRecording);
            recordButton.textContent = "Zakończ nagranie";
            recordButton.style.backgroundColor = "#d9534f";
            recordButton.addEventListener('click', stopRecording);
            recorder.start();
            timeLimit = setTimeout(stopRecording, 3500);
        }

        function stopRecording() {
            ilosc++;
            document.getElementById("liczbaNagran").innerText = "Liczba nagrań: " + ilosc;
            clearTimeout(timeLimit);
            recordButton.removeEventListener('click', stopRecording);
            recordButton.textContent = "Rozpocznij nagranie";
            recordButton.style.backgroundColor = "#5cb85c";
            recordButton.addEventListener('click', startRecording);
            recorder.stop();
        }

		function cleanUp(s)
		{
			s = s.replace(/ę/ig,'e');
			s = s.replace(/ż/ig,'z');
			s = s.replace(/ó/ig,'o');
			s = s.replace(/ł/ig,'l');
			s = s.replace(/ć/ig,'c');
			s = s.replace(/ś/ig,'s');
			s = s.replace(/ź/ig,'z');
			s = s.replace(/ń/ig,'n');
			s = s.replace(/ą/ig,'a');
			return s.replace(/[^a-zA-Z0-9]/g,'_'); // final clean up
		}
		
        function uploadAudio(e) {
            chunks.push(e.data)
            var rand = Math.floor((Math.random() * 10000000));
            var date = new Date();
            var fileName = cleanUp(selectedOption) + '-' + cleanUp(name) + '-' + date.getFullYear().toString() + '_' + pad2(date.getMonth() + 1) + '_' + pad2( date.getDate()) + '_' + pad2( date.getHours() ) + '_' + pad2( date.getMinutes() ) + '_' + pad2( date.getSeconds() ) + '-' + rand;// + ".wav"
            var blob = new Blob(chunks, {
                type: 'audio'
            });
            var url = URL.createObjectURL(blob);
            var formData = new FormData();
            formData.append('audio-filename', fileName);
            formData.append('audio-blob', blob);

            xhr('save.php', formData, function (fileURL) {
                //window.open(fileURL);
            });

            function xhr(url, data, callback) {
                var request = new XMLHttpRequest();
                request.onreadystatechange = function () {
                    if (request.readyState == 4 && request.status == 200) {
                        callback(location.href + request.responseText);
                    }
                };
                request.open('POST', url);
                request.send(data);
            }
            var audio = document.getElementById('audio');
            audio.src = window.URL.createObjectURL(e.data);
            var audioURL = audio.src;
            //downloadLink.href = audioURL;
            //downloadLink.innerHTML = audioURL;
            //downloadLink.setAttribute("download", fileName);
            //downloadLink.setAttribute("name", fileName);
            audio.play();
        }
    }
    
    function pad2(n) { return n < 10 ? '0' + n : n }

    </script>
	
	
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>