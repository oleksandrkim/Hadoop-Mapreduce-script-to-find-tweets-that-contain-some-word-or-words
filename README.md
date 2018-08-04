# Hadoop-Mapreduce-script-to-find-tweets-that-contain-some-word-or-words
This mapreduce task finds files where some code is stored. In this example every file is a tweet from Trumps twitter. I tried to find tweets where Trump used the name of US in some form (United States, US, USA etc.) or words Good and Bad.

Every tweet is stored in json file (for instance,   **js_0.json**) <br/>
The **mapreduce output**can be found in result.txt <br/>
The **log** file of the mapreduce - log.txt<br/>
The **jar** file used to run a mapreduce job - find_word_twitter_wordsinside.jar<br/>
Driver, Mapper and Reducer are saved as separate files for a reference<br/>
The code to **extract tweets from Twitter API** is in extract_tweet.py<br/>

**The code in hadoop to run a script**<br/>
Because data is stored in json, some additional libjar is needed to run the script - json-simple-1.1.jar <br/>

```hadoop jar /home/hirwuser864/findwordtwitter/find_word_twitter_wordsinside.jar com.mop.findword.findwordDriver -libjars /hirw-workshop/mapreduce/facebook/json-simple-1.1.jar /user/hirwuser864/findwordtwitter_input/input/ /user/hirwuser864/findwordtwitterwordsinside_output```


**Driver**

```
package com.mop.findword;

import org.apache.hadoop.conf.Configured;
import org.json.simple.parser.JSONParser;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
//import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import com.mop.findword.findwordDriver;
import com.mop.findword.findwordMapper;
import com.mop.findword.findwordReducer;


public class findwordDriver extends Configured implements Tool {


	
	@Override
	public int run(String[] args) throws Exception {
		
		if (args.length != 2) {
			System.err.println("Usage: libjar <input path> <output path>");
			System.exit(-1);
		}

		//Job Setup
		Job fb = Job.getInstance(getConf(), "findword");
		
		fb.setJarByClass(findwordDriver.class);
		
		
		//File Input and Output format
		FileInputFormat.addInputPath(fb, new Path(args[0]));
		FileOutputFormat.setOutputPath(fb, new Path(args[1]));
		
		fb.setInputFormatClass(TextInputFormat.class);
		fb.setOutputFormatClass(SequenceFileOutputFormat.class);

		//Output types
		
				
		fb.setMapperClass(findwordMapper.class);
		fb.setReducerClass(findwordReducer.class);
		

		fb.setOutputKeyClass(Text.class); //type of a key (stock code)
		fb.setOutputValueClass(Text.class); //type of a value (price); 
		
		//Submit job
		return fb.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {

		int exitCode = ToolRunner.run(new findwordDriver(), args);
		System.exit(exitCode);
	}}
```

<br>
   
**Mapper**

```
package com.mop.findword;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.apache.hadoop.mapreduce.Mapper;

public class findwordMapper extends Mapper<LongWritable, Text, Text, Text> {
	@Override //we need to overwrite "map" method;
	public void map(LongWritable key, Text value, Context context) 
			throws IOException, InterruptedException {
		String fileName = ((FileSplit) context.getInputSplit()).getPath().getName();

		String line = value.toString();
		Path pt=new Path("hdfs://ip-172-31-45-216.ec2.internal:8020/user/hirwuser864/findwordtwitter_words/words");
		FileSystem fs = FileSystem.get(context.getConfiguration());
		BufferedReader br=new BufferedReader(new InputStreamReader(fs.open(pt)));
		String words=br.readLine();
		String[] items = words.split(" ");
		//String[] items = {"US","USA","[Gg]ood","[Bb]ad"};
		for (int i = 0; i<items.length; i+=1 ) {
			
			String pattern = items[i];
			
			try {
				JSONParser parser = new JSONParser();
	            Object obj = parser.parse(line);
	 
	            JSONObject jsonObject = (JSONObject) obj;
	 
	            String full_text = (String) jsonObject.get("full_text");
			    Pattern r = Pattern.compile(pattern);

			    CharSequence cs = full_text; 
			    Matcher m = r.matcher(cs);
			    if (m.find( )) {
			    	context.write(new Text(items[i]), new Text(fileName));
				    
				    }
	 
			
	        } catch (IOException e) {
	            e.printStackTrace();
	        } catch (ParseException e) {
	            e.printStackTrace();
	        }
			
		      // Create a Pattern object

			
		}
		}
}
```
<br>
  
**Reducer**

```
package com.mop.findword;

import java.io.IOException;

//import org.apache.hadoop.io.DoubleWritable;
//import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class findwordReducer extends Reducer<Text, Text, Text, Text> {
	
	 @Override
	 public void reduce(Text key, Iterable<Text> values, Context context)
			 throws IOException, InterruptedException {
		 String result = "[";
		 for (Text value : values) {
			 result = result + ", " + value;
		 }
		 result = result + "]";
		 context.write(key, new Text(result));

	
	

	 }
}
```
<br>
  
**Log**

```
hirwuser864@ip-172-31-45-217:~$ hadoop jar /home/hirwuser864/findwordtwitter/find_word_twitter.jar com.mop.findword.findwordDriver -libjars /hirw-workshop/mapreduce/facebook/json-simple-1.1.jar /user/hirwuser864/findwordtwitter_input/input/ /user/hirwuser864/findwordtwitter_output
18/06/17 16:02:01 INFO client.RMProxy: Connecting to ResourceManager at ip-172-31-45-216.ec2.internal/172.31.45.216:8032
18/06/17 16:02:02 INFO input.FileInputFormat: Total input paths to process : 1000
18/06/17 16:02:02 INFO mapreduce.JobSubmitter: number of splits:1000
18/06/17 16:02:03 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1525967314796_1105
18/06/17 16:02:03 INFO impl.YarnClientImpl: Submitted application application_1525967314796_1105
18/06/17 16:02:03 INFO mapreduce.Job: The url to track the job: http://ec2-54-92-244-237.compute-1.amazonaws.com:8088/proxy/application_1525967314796_1105/
18/06/17 16:02:03 INFO mapreduce.Job: Running job: job_1525967314796_1105
18/06/17 16:02:09 INFO mapreduce.Job: Job job_1525967314796_1105 running in uber mode : false
18/06/17 16:02:09 INFO mapreduce.Job:  map 0% reduce 0%
18/06/17 16:02:22 INFO mapreduce.Job:  map 1% reduce 0%
18/06/17 16:02:38 INFO mapreduce.Job:  map 2% reduce 0%
18/06/17 16:02:53 INFO mapreduce.Job:  map 3% reduce 0%
18/06/17 16:03:08 INFO mapreduce.Job:  map 4% reduce 0%
18/06/17 16:03:25 INFO mapreduce.Job:  map 5% reduce 0%
18/06/17 16:03:42 INFO mapreduce.Job:  map 6% reduce 0%
18/06/17 16:03:58 INFO mapreduce.Job:  map 7% reduce 0%
18/06/17 16:04:13 INFO mapreduce.Job:  map 8% reduce 0%
18/06/17 16:04:28 INFO mapreduce.Job:  map 9% reduce 0%
18/06/17 16:04:46 INFO mapreduce.Job:  map 10% reduce 0%
18/06/17 16:05:02 INFO mapreduce.Job:  map 11% reduce 0%
18/06/17 16:05:15 INFO mapreduce.Job:  map 12% reduce 0%
18/06/17 16:05:31 INFO mapreduce.Job:  map 13% reduce 0%
18/06/17 16:05:48 INFO mapreduce.Job:  map 14% reduce 0%
18/06/17 16:06:06 INFO mapreduce.Job:  map 15% reduce 0%
18/06/17 16:06:22 INFO mapreduce.Job:  map 16% reduce 0%
18/06/17 16:06:38 INFO mapreduce.Job:  map 17% reduce 0%
18/06/17 16:06:55 INFO mapreduce.Job:  map 18% reduce 0%
18/06/17 16:07:10 INFO mapreduce.Job:  map 19% reduce 0%
18/06/17 16:07:27 INFO mapreduce.Job:  map 20% reduce 0%
18/06/17 16:07:43 INFO mapreduce.Job:  map 21% reduce 0%
18/06/17 16:07:56 INFO mapreduce.Job:  map 22% reduce 0%
18/06/17 16:08:14 INFO mapreduce.Job:  map 23% reduce 0%
18/06/17 16:08:30 INFO mapreduce.Job:  map 24% reduce 0%
18/06/17 16:08:45 INFO mapreduce.Job:  map 25% reduce 0%
18/06/17 16:09:02 INFO mapreduce.Job:  map 26% reduce 0%
18/06/17 16:09:14 INFO mapreduce.Job:  map 26% reduce 9%
18/06/17 16:09:18 INFO mapreduce.Job:  map 27% reduce 9%
18/06/17 16:09:34 INFO mapreduce.Job:  map 28% reduce 9%
18/06/17 16:09:50 INFO mapreduce.Job:  map 29% reduce 9%
18/06/17 16:09:56 INFO mapreduce.Job:  map 29% reduce 10%
18/06/17 16:10:07 INFO mapreduce.Job:  map 30% reduce 10%
18/06/17 16:10:22 INFO mapreduce.Job:  map 31% reduce 10%
18/06/17 16:10:39 INFO mapreduce.Job:  map 32% reduce 10%
18/06/17 16:10:44 INFO mapreduce.Job:  map 32% reduce 11%
18/06/17 16:10:55 INFO mapreduce.Job:  map 33% reduce 11%
18/06/17 16:11:11 INFO mapreduce.Job:  map 34% reduce 11%
18/06/17 16:11:29 INFO mapreduce.Job:  map 35% reduce 11%
18/06/17 16:11:32 INFO mapreduce.Job:  map 35% reduce 12%
18/06/17 16:11:46 INFO mapreduce.Job:  map 36% reduce 12%
18/06/17 16:11:59 INFO mapreduce.Job:  map 37% reduce 12%
18/06/17 16:12:15 INFO mapreduce.Job:  map 38% reduce 12%
18/06/17 16:12:21 INFO mapreduce.Job:  map 38% reduce 13%
18/06/17 16:12:34 INFO mapreduce.Job:  map 39% reduce 13%
18/06/17 16:12:48 INFO mapreduce.Job:  map 40% reduce 13%
18/06/17 16:13:03 INFO mapreduce.Job:  map 41% reduce 13%
18/06/17 16:13:09 INFO mapreduce.Job:  map 41% reduce 14%
18/06/17 16:13:23 INFO mapreduce.Job:  map 42% reduce 14%
18/06/17 16:13:36 INFO mapreduce.Job:  map 43% reduce 14%
18/06/17 16:13:52 INFO mapreduce.Job:  map 44% reduce 14%
18/06/17 16:13:57 INFO mapreduce.Job:  map 44% reduce 15%
18/06/17 16:14:11 INFO mapreduce.Job:  map 45% reduce 15%
18/06/17 16:14:27 INFO mapreduce.Job:  map 46% reduce 15%
18/06/17 16:14:43 INFO mapreduce.Job:  map 47% reduce 15%
18/06/17 16:14:45 INFO mapreduce.Job:  map 47% reduce 16%
18/06/17 16:14:59 INFO mapreduce.Job:  map 48% reduce 16%
18/06/17 16:15:14 INFO mapreduce.Job:  map 49% reduce 16%
18/06/17 16:15:32 INFO mapreduce.Job:  map 50% reduce 16%
18/06/17 16:15:34 INFO mapreduce.Job:  map 50% reduce 17%
18/06/17 16:15:48 INFO mapreduce.Job:  map 51% reduce 17%
18/06/17 16:16:04 INFO mapreduce.Job:  map 52% reduce 17%
18/06/17 16:16:20 INFO mapreduce.Job:  map 53% reduce 17%
18/06/17 16:16:22 INFO mapreduce.Job:  map 53% reduce 18%
18/06/17 16:16:36 INFO mapreduce.Job:  map 54% reduce 18%
18/06/17 16:16:52 INFO mapreduce.Job:  map 55% reduce 18%
18/06/17 16:17:08 INFO mapreduce.Job:  map 56% reduce 18%
18/06/17 16:17:10 INFO mapreduce.Job:  map 56% reduce 19%
18/06/17 16:17:28 INFO mapreduce.Job:  map 57% reduce 19%
18/06/17 16:17:45 INFO mapreduce.Job:  map 58% reduce 19%
18/06/17 16:18:01 INFO mapreduce.Job:  map 59% reduce 19%
18/06/17 16:18:04 INFO mapreduce.Job:  map 59% reduce 20%
18/06/17 16:18:17 INFO mapreduce.Job:  map 60% reduce 20%
18/06/17 16:18:35 INFO mapreduce.Job:  map 61% reduce 20%
18/06/17 16:18:54 INFO mapreduce.Job:  map 62% reduce 20%
18/06/17 16:18:58 INFO mapreduce.Job:  map 62% reduce 21%
18/06/17 16:19:10 INFO mapreduce.Job:  map 63% reduce 21%
18/06/17 16:19:30 INFO mapreduce.Job:  map 64% reduce 21%
18/06/17 16:19:46 INFO mapreduce.Job:  map 65% reduce 22%
18/06/17 16:20:02 INFO mapreduce.Job:  map 66% reduce 22%
18/06/17 16:20:18 INFO mapreduce.Job:  map 67% reduce 22%
18/06/17 16:20:36 INFO mapreduce.Job:  map 68% reduce 22%
18/06/17 16:20:40 INFO mapreduce.Job:  map 68% reduce 23%
18/06/17 16:20:55 INFO mapreduce.Job:  map 69% reduce 23%
18/06/17 16:21:13 INFO mapreduce.Job:  map 70% reduce 23%
18/06/17 16:21:30 INFO mapreduce.Job:  map 71% reduce 23%
18/06/17 16:21:34 INFO mapreduce.Job:  map 71% reduce 24%
18/06/17 16:21:46 INFO mapreduce.Job:  map 72% reduce 24%
18/06/17 16:22:01 INFO mapreduce.Job:  map 73% reduce 24%
18/06/17 16:22:19 INFO mapreduce.Job:  map 74% reduce 24%
18/06/17 16:22:23 INFO mapreduce.Job:  map 74% reduce 25%
18/06/17 16:22:37 INFO mapreduce.Job:  map 75% reduce 25%
18/06/17 16:22:55 INFO mapreduce.Job:  map 76% reduce 25%
18/06/17 16:23:13 INFO mapreduce.Job:  map 77% reduce 25%
18/06/17 16:23:17 INFO mapreduce.Job:  map 77% reduce 26%
18/06/17 16:23:31 INFO mapreduce.Job:  map 78% reduce 26%
18/06/17 16:23:43 INFO mapreduce.Job:  map 79% reduce 26%
18/06/17 16:24:01 INFO mapreduce.Job:  map 80% reduce 26%
18/06/17 16:24:05 INFO mapreduce.Job:  map 80% reduce 27%
18/06/17 16:24:19 INFO mapreduce.Job:  map 81% reduce 27%
18/06/17 16:24:37 INFO mapreduce.Job:  map 82% reduce 27%
18/06/17 16:24:55 INFO mapreduce.Job:  map 83% reduce 27%
18/06/17 16:24:59 INFO mapreduce.Job:  map 83% reduce 28%
18/06/17 16:25:13 INFO mapreduce.Job:  map 84% reduce 28%
18/06/17 16:25:27 INFO mapreduce.Job:  map 85% reduce 28%
18/06/17 16:25:43 INFO mapreduce.Job:  map 86% reduce 28%
18/06/17 16:25:47 INFO mapreduce.Job:  map 86% reduce 29%
18/06/17 16:26:02 INFO mapreduce.Job:  map 87% reduce 29%
18/06/17 16:26:20 INFO mapreduce.Job:  map 88% reduce 29%
18/06/17 16:26:38 INFO mapreduce.Job:  map 89% reduce 29%
18/06/17 16:26:42 INFO mapreduce.Job:  map 89% reduce 30%
18/06/17 16:26:56 INFO mapreduce.Job:  map 90% reduce 30%
18/06/17 16:27:14 INFO mapreduce.Job:  map 91% reduce 30%
18/06/17 16:27:29 INFO mapreduce.Job:  map 92% reduce 30%
18/06/17 16:27:35 INFO mapreduce.Job:  map 92% reduce 31%
18/06/17 16:27:45 INFO mapreduce.Job:  map 93% reduce 31%
18/06/17 16:28:01 INFO mapreduce.Job:  map 94% reduce 31%
18/06/17 16:28:20 INFO mapreduce.Job:  map 95% reduce 31%
18/06/17 16:28:23 INFO mapreduce.Job:  map 95% reduce 32%
18/06/17 16:28:37 INFO mapreduce.Job:  map 96% reduce 32%
18/06/17 16:28:52 INFO mapreduce.Job:  map 97% reduce 32%
18/06/17 16:29:09 INFO mapreduce.Job:  map 98% reduce 32%
18/06/17 16:29:11 INFO mapreduce.Job:  map 98% reduce 33%
18/06/17 16:29:25 INFO mapreduce.Job:  map 99% reduce 33%
18/06/17 16:29:41 INFO mapreduce.Job:  map 100% reduce 33%
18/06/17 16:29:51 INFO mapreduce.Job:  map 100% reduce 100%
18/06/17 16:29:51 INFO mapreduce.Job: Job job_1525967314796_1105 completed successfully
18/06/17 16:29:51 INFO mapreduce.Job: Counters: 53
        File System Counters
                FILE: Number of bytes read=3586
                FILE: Number of bytes written=125531392
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=444519
                HDFS: Number of bytes written=2124
                HDFS: Number of read operations=3003
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
        Job Counters
                Launched map tasks=1000
                Launched reduce tasks=1
                Data-local map tasks=1000
                Total time spent by all maps in occupied slots (ms)=17399300
                Total time spent by all reduces in occupied slots (ms)=5017684
                Total time spent by all map tasks (ms)=4349825
                Total time spent by all reduce tasks (ms)=1254421
                Total vcore-milliseconds taken by all map tasks=4349825
                Total vcore-milliseconds taken by all reduce tasks=1254421
                Total megabyte-milliseconds taken by all map tasks=4454220800
                Total megabyte-milliseconds taken by all reduce tasks=1284527104
        Map-Reduce Framework
                Map input records=1032
                Map output records=246
                Map output bytes=3088
                Map output materialized bytes=9580
                Input split bytes=157890
                Combine input records=0
                Combine output records=0
                Reduce input groups=6
                Reduce shuffle bytes=9580
                Reduce input records=246
                Reduce output records=6
                Spilled Records=492
                Shuffled Maps =1000
                Failed Shuffles=0
                Merged Map outputs=1000
                GC time elapsed (ms)=30408
                CPU time spent (ms)=405960
                Physical memory (bytes) snapshot=264764542976
                Virtual memory (bytes) snapshot=1378467610624
                Total committed heap usage (bytes)=188008628224
                Peak Map Physical memory (bytes)=304279552
                Peak Map Virtual memory (bytes)=1390415872
                Peak Reduce Physical memory (bytes)=404221952
                Peak Reduce Virtual memory (bytes)=1383501824
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=286629
        File Output Format Counters
                Bytes Written=2124
```

<br>
  
## Output

>Good    [, js_30, js_469, js_534, js_396, js_499, js_602, js_839, js_111, js_944, js_242]<br>  
>US      [, js_77, js_770, js_195, js_459, js_186, js_886, js_194, js_463, js_260, js_196, js_609, js_477, js_257, js_856, js_536, js_487, js_636, js_18, js_660, js_261, js_180, js_838, js_381, js_625, js_481, js_758, js_552, js_986, js_429, js_351, js_33, js_735, js_634, js_437, js_865, js_410, js_955, js_593, js_654, js_895, js_259, js_271, js_303, js_775, js_725, js_643, js_664, js_355, js_741, js_710, js_947, js_697, js_241, js_540, js_522, js_430, js_876, js_904, js_435]<br>  
>USA     [, js_895, js_381, js_838, js_593, js_955, js_634, js_33, js_437]<br>  
>[Bb]ad  [, js_51, js_359, js_490, js_440, js_684, js_645, js_217, js_393, js_212, js_848, js_731, js_517, js_910, js_893, js_335, js_106, js_3, js_412, js_353, js_322, js_956, js_139, js_377, js_580, js_553, js_546, js_835, js_244, js_482, js_154, js_15, js_811, js_789, js_118, js_585, js_650, js_373, js_826, js_810, js_901, js_612, js_549, js_170]<br>  
>[Gg]ood [, js_379, js_166, js_491, js_40, js_867, js_922, js_602, js_756, js_30, js_51, js_242, js_528, js_45, js_389, js_43, js_706, js_11, js_731, js_99, js_516, js_611, js_3, js_572, js_464, js_849, js_499, js_809, js_641, js_604, js_797, js_839, js_475, js_699, js_352, js_515, js_381, js_838, js_792, js_396, js_219, js_527, js_251, js_944, js_783, js_518, js_422, js_750, js_326, js_318, js_169, js_992, js_466, js_208, js_469, js_632, js_636, js_217, js_72, js_218, js_111, js_766, js_455, js_534, js_541, js_291, js_188, js_517, js_178]<br>  
good    [, js_178, js_72, js_636, js_632, js_169, js_318, js_750, js_422, js_251, js_527, js_792, js_838, js_475, js_379, js_604, js_641, js_849, js_464, js_3, js_611, js_11, js_706, js_389, js_45, js_51, js_867, js_922, js_491, js_541, js_218, js_766, js_217, js_992, js_326, js_783, js_219, js_699, js_797, js_166, js_572, js_731, js_43, js_40, js_756, js_291, js_455, js_466, js_518, js_352, js_809, js_99, js_528, js_188, js_208, js_515, js_516, js_517, js_381]<br>  
