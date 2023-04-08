package com.yazlab.stringconcat;

import com.mongodb.client.*;
import org.bson.Document;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import java.io.File;
import java.io.FileWriter;
import java.util.List;
import java.util.Map;


import static com.yazlab.stringconcat.concatenation.sortStringsAndConcat;

@SpringBootApplication
@RestController
@EnableMongoRepositories
public class StringconcatApplication {

    @Autowired
    private StringRepository stringRepository;
    @Autowired
    private MongoTemplate mongoTemplate;

    public static void main(String[] args) {
        SpringApplication.run(StringconcatApplication.class, args);
    }

    @GetMapping("/send")
    public ModelAndView sendWords(@RequestParam("words[]") List<String> words) {
        // Create an unmodifiable copy of the words
        List<String> unsorted = List.copyOf(words);

        // make words all lowercase
        words.replaceAll(String::toLowerCase);

        // Sort the words and get the duration
        long startTime = System.nanoTime();
        String result = sortStringsAndConcat(words);
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1000000.0;

        // Create a new ModelAndView and add the words, result and duration to it
        ModelAndView modelAndView = new ModelAndView("send");
        modelAndView.addObject("words", unsorted);
        modelAndView.addObject("result", result);
        modelAndView.addObject("duration", duration);

        return modelAndView;
    }

    @PostMapping("/save")
    public ResponseEntity<String> saveString(@RequestBody Map<String, Object> payload) {
        System.out.println(payload);

        // Get the words, result and duration from the payload
        String sentencesString = (String) payload.get("words");
        String result = (String) payload.get("result");
        String durationString = (String) payload.get("duration");

        // Convert the words to a list and the duration to a double
        List<String> sentences = List.of(sentencesString.split("\n"));
        double duration = Double.parseDouble(durationString);

        // Create a new Strings object and save it to the database
        Strings newEntry = new Strings(sentences, result, duration);
        stringRepository.save(newEntry);

        return ResponseEntity.ok(result);
    }

    @GetMapping("/export")
    public ResponseEntity<String> exportMongoDbCollection() {
        try {
            // Get the collection from MongoDB
            MongoCollection<Document> collection = mongoTemplate.getCollection("strings");

            // Create a cursor to iterate over the documents in the collection
            MongoCursor<Document> cursor = collection.find().iterator();

            // Create a JSON array to hold the documents
            JSONArray jsonArray = new JSONArray();

            // Iterate over the documents and add them to the JSON array
            while (cursor.hasNext()) {
                Document document = cursor.next();
                JSONObject jsonObject = new JSONObject(document.toJson());
                jsonArray.put(jsonObject);
            }

            // Write the JSON array to a file in the project's folder
            File file = new File("strings.json");
            FileWriter fileWriter = new FileWriter(file);
            fileWriter.write(jsonArray.toString(2));
            fileWriter.flush();
            fileWriter.close();

            System.out.println("Collection exported to strings.json file.");
            return ResponseEntity.ok("Collection exported to strings.json file.");
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }
    }

}
