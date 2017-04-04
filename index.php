<html>
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Audio recording">
    <meta name="keywords" content="HTML,CSS,JavaScript">
    <meta name="author" content="Przemyslaw Wegrzynowicz">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title> Voice recording</title>


<link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/bootstrap-theme.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="css/theme.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]-->
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>

</head>

<body>

<div class = "container">
<?php
$ua = strtolower($_SERVER['HTTP_USER_AGENT']);
if(stripos($ua,'android') == false) { // && stripos($ua,'mobile') !== false) {
?>	<nav class="navbar navbar-inverse">
		<div class="container-fluid">
			<div class="navbar-header">
				<a class="navbar-brand" href="#">Strona Główna</a>
            </div>
            
          <ul class="nav navbar-nav">
            	<li><a href="#">Nagraj dźwięk</a></li>
                <li><a href="#">O Projekcie</a></li>
                <li><a href="#">Kontakt</a></li>
            </ul>
        </div>
	</nav>
	</div>
        <div class ="container">
		<div class="jumbotron">
        	<h2>Rozpoznawanie mowy</h2>
            <p>
            Rozpoznawanie mowy to młody i wciąż eksplorowany temat. 
			Nie ma obecnie na rynku doskonałego rozwiązania, które byłoby wzorem dla konkurencji. 
			Niemniej jednak każdy z dostępnych programów ma wiele do zaoferowania swoim użytkownikom. 
			Dzięki takim aplikacjom używanie klawiatury i myszy jest opcjonalne. 
			Zamiast tego można sterować komputerem za pomocą głosu i dyktować tekst.
            </p>
            <img src="images/text_separator.png" />
            <p>
            Wypróbuj rozpoznawanie mowy.
            </p>
        
       
	</div>
	</div>
    <div class="container">
  
    <?php
    }else{
        ?>
        <div class="container">
    <?php
    }
    ?>
    
     <div class = "well" id="boxy_content">
		<h2>Nagrywanie mowy</h2>
		
		<form id="Formularz" name="Formularz" action="nagraj.php" method="post"onsubmit="return false;">
		<div class="form-group">
		<label for = "imie">Imię i Nazwisko</label><input type="text" name="imie" id="imie" />
		</div>
		
		<div class="form-group">
		
		<label for ="optionList">Komenda</label>
		<select name="Komenda" id="optionList">
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
		</div>
	</div>

	</body>
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
        var optionList = document.getElementById("optionList");
        selectedOption = optionList.options[optionList.selectedIndex].text;
        var recordDiv = document.getElementById("boxy_content");
        recordDiv.innerHTML = '<h2>Nagrywanie mowy</h2>\
            <h2> Jako: ' + name + '</h2>\
            <h2> Czynność: ' + selectedOption + '<h2>\
            <button class="btn btn-success btn-lg" id="record" disabled > Rozpocznij </button><br>\
            <audio id="audio" controls></audio><br>\
            <button type="button" class="btn btn-primary btn-lg " onclick="location.reload()" > Wybierz inną czynność</button>\
            <a id="downloadLink" href></a>';
        
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
                    recordButton.style.backgroundColor = "#00ff00";
                    recordButton.addEventListener('click', startRecording);
                    //stopButton.addEventListener('click', stopRecording);
                    recorder = new MediaRecorder(stream);
                    recorder.ondataavailable = uploadAudio
                });

        function startRecording() {
            chunks = [];
            recordButton.removeEventListener('click', startRecording);
            recordButton.textContent = "Zakończ";
            recordButton.style.backgroundColor = "#ff0000";
            recordButton.addEventListener('click', stopRecording);
            recorder.start();
            timeLimit = setTimeout(stopRecording, 3500);
        }

        function stopRecording() {
            clearTimeout(timeLimit);
            recordButton.removeEventListener('click', stopRecording);
            recordButton.textContent = "Rozpocznij";
            recordButton.style.backgroundColor = "#00ff00";
            recordButton.addEventListener('click', startRecording);
            recorder.stop();
        }

        function uploadAudio(e) {
            chunks.push(e.data)
            var rand = Math.floor((Math.random() * 10000000));
            var date = new Date();
            var fileName = selectedOption + '-' + name.replace(/\s/g,'') + '-' + date.getFullYear().toString() + '_' + pad2(date.getMonth() + 1) + '_' + pad2( date.getDate()) + '_' + pad2( date.getHours() ) + '_' + pad2( date.getMinutes() ) + '_' + pad2( date.getSeconds() ) + '-' + rand + ".wav";
            var blob = new Blob(chunks, {
                type: 'audio/wav'
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
            downloadLink.href = audioURL;
            downloadLink.innerHTML = audioURL;
            downloadLink.setAttribute("download", fileName);
            downloadLink.setAttribute("name", fileName);
            audio.play();
        }
    }
    
    function pad2(n) { return n < 10 ? '0' + n : n }

    </script>
</html>