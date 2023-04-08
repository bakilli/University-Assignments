package com.yazlab.stringconcat;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.List;

public interface StringRepository extends MongoRepository<Strings, String> {
    @Query("{ 'strings' : ?0 }")
    Strings findByStrings(List<String> strings);

    @Query("{ 'result' : ?0 }")
    Strings findByResult(String result);


}
