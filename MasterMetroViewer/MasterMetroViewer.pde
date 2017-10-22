BufferedReader reader;
String line;
 
void setup() {
  // make an instance of File class to access data files with BufferedReader 
  File dir = new File(sketchPath());
  
  // Open the file from the createWriter() example
  reader = createReader("result-171022-182707.txt");   
  size(displayWidth,200);
  background(255);
  fill(0);
  frameRate(40);
}
 
void draw() {
  background(255);
  try {
    line = reader.readLine();
  } catch (IOException e) {
    e.printStackTrace();
    line = null;
  }
  if (line == null) {
    // Stop reading because of an error or file is empty
    noLoop();  
  } else {
    //println(line);
    String[] part = split(line, ' ');
    //println(part[1]);
    textSize(10);
    text(part[0], 10, 10);
    textSize(8.8);
    text(part[1], 2, 100);
  }
} 