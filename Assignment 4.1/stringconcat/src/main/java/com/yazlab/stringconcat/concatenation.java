package com.yazlab.stringconcat;

import java.util.*;

public class concatenation {
    static boolean debug = false;

    public static String sortStringsAndConcat(List<String> unsorted) {
        List<String> testForEntry = List.copyOf(unsorted);
        int countOfWords = 0;
        for (String s : testForEntry) {
            if (s.split(" ").length == 1) {
                countOfWords++;
            }
        }
        if (countOfWords == testForEntry.size()) {
            return ConcatForWords(unsorted);
        }
        // early return if there is only one sentence

        // remove short sentences that are contained in longer sentences
        ArrayList<String> unsortedCopy = new ArrayList<>(unsorted);
        for (int i = 0; i < unsortedCopy.size(); i++) {
            for (int j = 0; j < unsortedCopy.size(); j++) {
                if (i != j && unsortedCopy.get(i).length() < unsortedCopy.get(j).length() && unsortedCopy.get(j).contains(unsortedCopy.get(i))) {
                    unsortedCopy.remove(i);
                    i--;
                    break;
                }
            }
        }
        unsorted = unsortedCopy;
        // sort sentences
        unsorted.sort((s1, s2) -> {
            String[] words1 = s1.split(" ");
            String[] words2 = s2.split(" ");
            int minLength = Math.min(words1.length, words2.length);
//                for (int i = 0; i < minLength; i++) {
//                    int wordCompare = words1[i].compareTo(words2[i]);
//                    if (wordCompare != 0) {
//                        return wordCompare;
//                    }
//                }
            for (int i = 0; i < words1.length; i++) {
                for (int j = 0; j < words2.length; j++) {
                    if (words1[i].equals(words2[j])) {
                        int numberofequals = 1;
                        while (i + numberofequals < words1.length && j + numberofequals < words2.length && words1[i + numberofequals].equals(words2[j + numberofequals])) {
                            numberofequals++;
                        }
                        if (i + numberofequals < words1.length && j + numberofequals < words2.length) {
                            return words1[i + numberofequals].compareTo(words2[j + numberofequals]);
                            //System.out.println("words1[i + numberofequals] = " + words1[i + numberofequals]);
//                                if (minLength == words1.length)
//                                    return 1;
//                                else
//                                    return -1;
                        } else if (i + numberofequals < words1.length) {
                            return 1;
                        } else if (j + numberofequals < words2.length) {
                            return -1;
                        }

                    }
                }
            }
            return 0;
//            return Integer.compare(words1.length, words2.length);
        });
        return ConcatForSentences(unsorted);
    }

    public static String ConcatForWords(List<String> words) {
        StringBuilder sb = new StringBuilder();
        char[][] wordChars = new char[words.size()][];
        for (int i = 0; i < words.size(); i++) {
            wordChars[i] = words.get(i).toCharArray();
        }
        Set<Character> commonChars = new HashSet<>();
        for (char c : wordChars[0]) {
            commonChars.add(c);
        }
        for (int i = 1; i < wordChars.length; i++) {
            Set<Character> temp = new HashSet<>();
            for (char c : wordChars[i]) {
                temp.add(c);
            }
            commonChars.retainAll(temp);
        }
        for (char c : wordChars[wordChars.length - 1]) {
            if (commonChars.contains(c)) {
                sb.append(c);
            }
        }
        // append the rest of the word for the final input
        for (int i = 0; i < wordChars[wordChars.length - 1].length; i++) {
            if (!commonChars.contains(wordChars[wordChars.length - 1][i])) {
                sb.append(wordChars[wordChars.length - 1][i]);
            }
        }
        if (debug) {
            System.out.println("words:");
            System.out.println(words);
            System.out.println("result:");
            System.out.println(sb);
        }
        return sb.toString();
    }

    public static String ConcatForSentences(List<String> words) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.size(); i++) {
            String word = words.get(i);
            if (i == 0) {
                sb.append(word);
            } else {
                String[] seperated = sb.toString().split(" ");
                for (int j = 0; j < seperated.length; j++) {
                    String suffix = seperated[j];
                    if (word.startsWith(suffix)) {
                        StringBuilder lenghtofSuffix = new StringBuilder();
                        for (int k = j; k < seperated.length; k++) {
                            lenghtofSuffix.append(seperated[k]);
                            lenghtofSuffix.append(" ");
                        }
                        lenghtofSuffix.deleteCharAt(lenghtofSuffix.length() - 1);
                        if (word.length() > lenghtofSuffix.length()) { // out of bounds exception
                            sb.append(word.substring(lenghtofSuffix.length()));
                        } else {
                            sb.append(" ").append(word);
                        }
                        break;
                    }
                    if (j == seperated.length - 1) {
                        sb.append(" ").append(word);
                    }
                }


            }
        }
        if (debug) {
            System.out.println("words:");
            System.out.println(words);
            System.out.println("result:");
            System.out.println(sb);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        debug = true;
        List<String> test = Arrays.asList("ali eve gel", "sonra", "eve gel sonra çarşı", "çarşıya git");
        List<String> test01 = Arrays.asList("ali eve gel", "eve gel sonra çarşı", "çarşıya git", "eve gel sonra");
        List<String> test2 = Arrays.asList("abcdefgh", "abcefgh", "abcdfghij");
        List<String> test3 = Arrays.asList("ali eve geldi kapıyı açtı", "kapıyı açtı ve eve girdi", "merdivenden çıktı ve ali eve geldi");
        List<String> test4 = Arrays.asList("merdivenden çıktı ve ali eve geldi", "ali eve geldi kapıyı açtı", "kapıyı açtı ve eve girdi");
        List<String> test5 = Arrays.asList("jonah gone to cinema", "to cinema and ate burger", "jonah likes to watch");
        List<String> test6 = Arrays.asList("ali veli eve git", "ali sana git eve dedim");
        List<String> test7 = Arrays.asList("ahmet eve gel", "eve gel","gelip", "gel seneye", "gelince gel");

        // time this function call in milliseconds
        long startTime = System.nanoTime();
        sortStringsAndConcat(test4);
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1000000.0;
        System.out.println("duration: " + duration + " ms");
    }
}
