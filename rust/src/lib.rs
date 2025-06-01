use std::collections::HashMap;
use std::time::Instant;
use std::io::{self, Write};
use std::sync::{Arc, Mutex, atomic::{AtomicBool, AtomicI32, Ordering}};
use std::thread;
use std::time::Duration;
use regex::Regex;
use rand::prelude::*;
use crossbeam::channel::unbounded;

pub const PUNCTUATION_CHARS: &str = ",-'.!";
const LETTER_CHARS: &str = "abcdefghijklmnopqrstuvwxyz";

fn format_with_commas(n: i32) -> String {
    let s = n.to_string();
    let chars: Vec<char> = s.chars().collect();
    let mut result = String::new();
    
    for (i, c) in chars.iter().enumerate() {
        if i > 0 && (chars.len() - i) % 3 == 0 {
            result.push(',');
        }
        result.push(*c);
    }
    result
}

lazy_static::lazy_static! {
    static ref INT_TO_WORD: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();
        m.insert("0", "zero");
        m.insert("1", "one");
        m.insert("2", "two");
        m.insert("3", "three");
        m.insert("4", "four");
        m.insert("5", "five");
        m.insert("6", "six");
        m.insert("7", "seven");
        m.insert("8", "eight");
        m.insert("9", "nine");
        m.insert("10", "ten");
        m.insert("11", "eleven");
        m.insert("12", "twelve");
        m.insert("13", "thirteen");
        m.insert("14", "fourteen");
        m.insert("15", "fifteen");
        m.insert("16", "sixteen");
        m.insert("17", "seventeen");
        m.insert("18", "eighteen");
        m.insert("19", "nineteen");
        m.insert("20", "twenty");
        m.insert("30", "thirty");
        m.insert("40", "forty");
        m.insert("50", "fifty");
        m.insert("60", "sixty");
        m.insert("70", "seventy");
        m.insert("80", "eighty");
        m.insert("90", "ninety");
        m
    };

    static ref WORD_TO_INT: HashMap<&'static str, i32> = {
        let mut m = HashMap::new();
        m.insert("zero", 0);
        m.insert("single", 1);
        m.insert("one", 1);
        m.insert("two", 2);
        m.insert("three", 3);
        m.insert("four", 4);
        m.insert("five", 5);
        m.insert("six", 6);
        m.insert("seven", 7);
        m.insert("eight", 8);
        m.insert("nine", 9);
        m.insert("ten", 10);
        m.insert("eleven", 11);
        m.insert("twelve", 12);
        m.insert("thirteen", 13);
        m.insert("fourteen", 14);
        m.insert("fifteen", 15);
        m.insert("sixteen", 16);
        m.insert("seventeen", 17);
        m.insert("eighteen", 18);
        m.insert("nineteen", 19);
        m.insert("twenty", 20);
        m.insert("thirty", 30);
        m.insert("forty", 40);
        m.insert("fifty", 50);
        m.insert("sixty", 60);
        m.insert("seventy", 70);
        m.insert("eighty", 80);
        m.insert("ninety", 90);
        m
    };

    static ref CHAR_TO_WORD: HashMap<char, &'static str> = {
        let mut m = HashMap::new();
        for c in LETTER_CHARS.chars() {
            m.insert(c, match c {
                'a' => "a", 'b' => "b", 'c' => "c", 'd' => "d", 'e' => "e", 'f' => "f",
                'g' => "g", 'h' => "h", 'i' => "i", 'j' => "j", 'k' => "k", 'l' => "l",
                'm' => "m", 'n' => "n", 'o' => "o", 'p' => "p", 'q' => "q", 'r' => "r",
                's' => "s", 't' => "t", 'u' => "u", 'v' => "v", 'w' => "w", 'x' => "x",
                'y' => "y", 'z' => "z", _ => ""
            });
        }
        m.insert(',', "comma");
        m.insert('-', "hyphen");
        m.insert('\'', "apostrophe");
        m.insert('.', "period");
        m.insert('!', "!");
        m
    };

    static ref WORD_TO_CHAR: HashMap<&'static str, char> = {
        let mut m = HashMap::new();
        for c in LETTER_CHARS.chars() {
            m.insert(match c {
                'a' => "a", 'b' => "b", 'c' => "c", 'd' => "d", 'e' => "e", 'f' => "f",
                'g' => "g", 'h' => "h", 'i' => "i", 'j' => "j", 'k' => "k", 'l' => "l",
                'm' => "m", 'n' => "n", 'o' => "o", 'p' => "p", 'q' => "q", 'r' => "r",
                's' => "s", 't' => "t", 'u' => "u", 'v' => "v", 'w' => "w", 'x' => "x",
                'y' => "y", 'z' => "z", _ => ""
            }, c);
        }
        m.insert("comma", ',');
        m.insert("hyphen", '-');
        m.insert("apostrophe", '\'');
        m.insert("period", '.');
        m.insert("!", '!');
        m
    };
}

pub fn num_to_words(num: i32) -> String {
    match num {
        0..=20 => INT_TO_WORD[num.to_string().as_str()].to_string(),
        21..=99 if num % 10 == 0 => INT_TO_WORD[num.to_string().as_str()].to_string(),
        21..=99 => format!("{}-{}", INT_TO_WORD[(num / 10 * 10).to_string().as_str()], INT_TO_WORD[(num % 10).to_string().as_str()]),
        100..=999 if num % 100 == 0 => format!("{} hundred", INT_TO_WORD[(num / 100).to_string().as_str()]),
        100..=999 => format!("{} hundred and {}", INT_TO_WORD[(num / 100).to_string().as_str()], num_to_words(num % 100)),
        1000..=9999 if num % 1000 == 0 => format!("{} thousand", INT_TO_WORD[(num / 1000).to_string().as_str()]),
        1000..=9999 => format!("{} thousand {}", INT_TO_WORD[(num / 1000).to_string().as_str()], num_to_words(num % 1000)),
        10000 => "ten thousand".to_string(),
        _ => "more than ten thousand".to_string(),
    }
}

pub fn words_to_num(words: &str) -> Result<i32, String> {
    let words_lower = words.to_lowercase();
    let word_list: Vec<&str> = words_lower.split(&['-', ' '][..]).collect();
    if word_list.len() > 2 {
        return Err(format!("Cannot yet parse number words of greater than 2 words. {:?} is too long.", word_list));
    }
    
    let mut num = 0;
    for word in word_list {
        if let Some(&val) = WORD_TO_INT.get(word) {
            num += val;
        } else {
            return Err(format!("Unknown word: {}", word));
        }
    }
    Ok(num)
}

pub struct Autogram {
    pub prefix: String,
    pub suffix: String,
    pub epoch: i32,
    pub update_all_counts: bool,
    pub make_plural: bool,
    pub include_final_and: bool,
    pub is_pangram: bool,
    pub include_punctuation: bool,
    pub countable_chars: String,
    pub counts: HashMap<char, i32>,
}

impl Autogram {
    pub fn new(prefix: &str, suffix: &str) -> Self {
        let mut ag = Self {
            prefix: prefix.to_string(),
            suffix: suffix.to_string(),
            epoch: 0,
            update_all_counts: true,
            make_plural: true,
            include_final_and: true,
            is_pangram: false,
            include_punctuation: false,
            countable_chars: String::new(),
            counts: HashMap::new(),
        };
        ag.countable_chars = ag.get_countable_chars();
        ag.counts = ag.get_counts();
        ag
    }

    fn get_counts(&self) -> HashMap<char, i32> {
        if self.is_pangram {
            LETTER_CHARS.chars().map(|c| (c, 1)).collect()
        } else if !self.prefix.is_empty() || !self.suffix.is_empty() {
            self.count_occurrences(&format!("{}{}", self.prefix, self.suffix))
        } else {
            let mut counts = HashMap::new();
            let mut rng = thread_rng();
            let random_char = LETTER_CHARS.chars().choose(&mut rng).unwrap();
            counts.insert(random_char, 1);
            counts
        }
    }

    fn get_countable_chars(&self) -> String {
        let mut chars = LETTER_CHARS.to_string();
        if self.include_punctuation {
            chars.push_str(PUNCTUATION_CHARS);
        }
        chars
    }

    fn counts_as_phrases(&self, counts: &HashMap<char, i32>) -> Vec<String> {
        counts.iter()
            .filter(|(_, &count)| count != 0)
            .map(|(&ch, &count)| {
                let word = CHAR_TO_WORD[&ch];
                let plural = if self.make_plural && count > 1 { "'s" } else { "" };
                format!("{} {}{}", num_to_words(count), word, plural)
            })
            .collect()
    }

    pub fn sentence(&self) -> String {
        let phrases = self.counts_as_phrases(&self.counts);
        let mut s = if !self.prefix.is_empty() {
            format!("{} ", self.prefix)
        } else {
            String::new()
        };

        if phrases.len() > 1 {
            s.push_str(&phrases[..phrases.len()-1].join(", "));
            if self.include_final_and {
                s.push_str(", and ");
            } else {
                s.push_str(", ");
            }
            s.push_str(&phrases[phrases.len()-1]);
        } else if !phrases.is_empty() {
            s.push_str(&phrases[0]);
        }

        if !self.suffix.is_empty() {
            s.push_str(&format!(", {}", self.suffix));
        } else if !self.prefix.is_empty() {
            s.push('.');
        }

        s
    }

    pub fn is_autogram(&self) -> bool {
        let sentence_counts = self.count_occurrences(&self.sentence());
        sentence_counts == self.counts
    }

    pub fn count_occurrences(&self, s: &str) -> HashMap<char, i32> {
        let lower_s = s.to_lowercase();
        self.countable_chars.chars()
            .filter_map(|ch| {
                let count = lower_s.matches(ch).count() as i32;
                if count > 0 { Some((ch, count)) } else { None }
            })
            .collect()
    }

    pub fn update_counts(&mut self, rand_char: bool) {
        if !rand_char {
            self.counts = self.count_occurrences(&self.sentence());
        } else {
            let keys: Vec<char> = self.counts.keys().cloned().collect();
            if !keys.is_empty() {
                let mut rng = thread_rng();
                let ch = keys.choose(&mut rng).unwrap();
                self.counts.insert(*ch, self.sentence().to_lowercase().matches(*ch).count() as i32);
            }
        }
        self.epoch += 1;
    }

    fn counts_to_str(&self) -> String {
        self.countable_chars.chars()
            .map(|ch| self.counts.get(&ch).unwrap_or(&0).to_string())
            .collect::<Vec<_>>()
            .join("")
    }

    pub fn search(&mut self, find_cycle: bool) -> String {
        self.countable_chars = self.get_countable_chars();
        self.counts = self.get_counts();
        self.epoch = 0;
        let mut search_complete = false;

        let mut update_random_char = false;
        let mut prev_sentences = std::collections::HashSet::new();
        let mut cycle_sentences = Vec::new();
        let mut in_cycle = false;

        println!("Iterating sentences to find {}", 
            if find_cycle { "a cycle" } 
            else if self.is_pangram { "a pangram" } 
            else { "an autogram" });
        println!("Starting sentence: {}", self.sentence());
        
        let mut print_epoch_counter = 0;
        let start_time = Instant::now();

        while !search_complete {
            self.update_counts(update_random_char);

            search_complete = if find_cycle {
                cycle_sentences.contains(&self.sentence())
            } else {
                self.is_autogram()
            };

            if in_cycle {
                cycle_sentences.push(self.sentence());
            } else if find_cycle {
                let count_str = self.counts_to_str();
                in_cycle = prev_sentences.contains(&count_str);
                prev_sentences.insert(count_str);
                if in_cycle {
                    println!("Found a cycle of len {} or smaller", prev_sentences.len() - 1);
                }
            }

            if print_epoch_counter > 9998 {
                print!("\rEpoch: {}", format_with_commas(self.epoch));
                io::stdout().flush().unwrap();
                print_epoch_counter = -1;
                if find_cycle && !in_cycle {
                    prev_sentences.clear();
                }
            }

            if !find_cycle {
                update_random_char = !update_random_char;
            }

            print_epoch_counter += 1;
        }

        let elapsed = start_time.elapsed();
        println!("\rEpoch: {}", format_with_commas(self.epoch));
        
        if find_cycle {
            println!("Found cycle of period {}", cycle_sentences.len() - 1);
            for (i, sentence) in cycle_sentences.iter().enumerate() {
                println!("Sentence {}: {}", i, sentence);
            }
            cycle_sentences.join("\n")
        } else {
            println!("Found an autogram!");
            println!("Total time: {} minutes {} seconds", elapsed.as_secs() / 60, elapsed.as_secs() % 60);
            println!("Raw count dictionary: {:?}", self.counts);
            println!("\n{}\n", self.sentence());
            self.sentence()
        }
    }

    pub fn search_parallel(&mut self, find_cycle: bool) -> String {
        let num_threads = num_cpus::get();
        println!("Starting parallel search with {} threads", num_threads);
        
        self.countable_chars = self.get_countable_chars();
        self.counts = self.get_counts();
        
        let (result_tx, result_rx) = unbounded();
        let stop_flag = Arc::new(AtomicBool::new(false));
        let thread_epochs = Arc::new(Mutex::new((0..num_threads).map(|_| AtomicI32::new(0)).collect::<Vec<_>>()));
        
        println!("Iterating sentences to find {}", 
            if find_cycle { "a cycle" } 
            else if self.is_pangram { "a pangram" } 
            else { "an autogram" });
        println!("Starting sentence: {}", self.sentence());
        println!();

        let start_time = Instant::now();
        let mut handles = vec![];
        
        for thread_id in 0..num_threads {
            let mut ag = Autogram::new(&self.prefix, &self.suffix);
            ag.make_plural = self.make_plural;
            ag.include_final_and = self.include_final_and;
            ag.is_pangram = self.is_pangram;
            ag.include_punctuation = self.include_punctuation;
            
            let result_tx = result_tx.clone();
            let stop_flag = Arc::clone(&stop_flag);
            let thread_epochs = Arc::clone(&thread_epochs);
            
            let handle = thread::spawn(move || {
                ag.search_worker(thread_id, find_cycle, result_tx, stop_flag, thread_epochs)
            });
            handles.push(handle);
        }

        drop(result_tx);

        let display_handle = {
            let thread_epochs = Arc::clone(&thread_epochs);
            let stop_flag = Arc::clone(&stop_flag);
            thread::spawn(move || {
                while !stop_flag.load(Ordering::Relaxed) {
                    thread::sleep(Duration::from_millis(500));
                    if !stop_flag.load(Ordering::Relaxed) {
                        Self::display_progress(&thread_epochs, num_threads);
                    }
                }
            })
        };

        let result = if let Ok((thread_id, result)) = result_rx.recv() {
            stop_flag.store(true, Ordering::Relaxed);
            let elapsed = start_time.elapsed();
            
            // Calculate total iterations across all threads
            let total_iterations = if let Ok(epochs) = thread_epochs.lock() {
                epochs.iter().map(|epoch| epoch.load(Ordering::Relaxed) as u64).sum::<u64>()
            } else {
                0
            };
            
            println!("\n🎉 Thread {} found the solution!", thread_id + 1);
            println!("{}", result);
            
            // Report performance metrics
            let elapsed_secs = elapsed.as_secs_f64();
            let iterations_per_second = if elapsed_secs > 0.0 {
                total_iterations as f64 / elapsed_secs
            } else {
                0.0
            };
            
            println!("Total iterations across all threads: {}", format_with_commas(total_iterations as i32));
            println!("Total time: {:.3} seconds ({} minutes {} seconds)", 
                elapsed_secs, elapsed.as_secs() / 60, elapsed.as_secs() % 60);
            println!("Total iterations per second: {}", format_with_commas(iterations_per_second as i32));
            
            result
        } else {
            "No solution found".to_string()
        };

        for handle in handles {
            let _ = handle.join();
        }
        let _ = display_handle.join();

        result
    }

    fn search_worker(
        &mut self,
        thread_id: usize,
        find_cycle: bool,
        result_tx: crossbeam::channel::Sender<(usize, String)>,
        stop_flag: Arc<AtomicBool>,
        thread_epochs: Arc<Mutex<Vec<AtomicI32>>>,
    ) {
        self.countable_chars = self.get_countable_chars();
        self.counts = self.get_counts();
        self.epoch = 0;
        
        let mut rng = thread_rng();
        if !self.is_pangram && self.prefix.is_empty() && self.suffix.is_empty() {
            let random_char = LETTER_CHARS.chars().choose(&mut rng).unwrap();
            self.counts.clear();
            self.counts.insert(random_char, 1);
        }

        let mut update_random_char = false;
        let mut prev_sentences = std::collections::HashSet::new();
        let mut cycle_sentences = Vec::new();
        let mut in_cycle = false;

        while !stop_flag.load(Ordering::Relaxed) {
            self.update_counts(update_random_char);

            if let Ok(epochs) = thread_epochs.lock() {
                epochs[thread_id].store(self.epoch, Ordering::Relaxed);
            }

            let search_complete = if find_cycle {
                cycle_sentences.contains(&self.sentence())
            } else {
                self.is_autogram()
            };

            if search_complete {
                let result = if find_cycle {
                    format!("Found cycle of period {}\n{}", 
                        cycle_sentences.len() - 1,
                        cycle_sentences.iter().enumerate()
                            .map(|(i, s)| format!("Sentence {}: {}", i, s))
                            .collect::<Vec<_>>()
                            .join("\n"))
                } else {
                    format!("Found an autogram!\nRaw count dictionary: {:?}\n\n{}\n", 
                        self.counts, self.sentence())
                };
                let _ = result_tx.send((thread_id, result));
                return;
            }

            if in_cycle {
                cycle_sentences.push(self.sentence());
            } else if find_cycle {
                let count_str = self.counts_to_str();
                in_cycle = prev_sentences.contains(&count_str);
                prev_sentences.insert(count_str);
                if in_cycle {
                    cycle_sentences.clear();
                    cycle_sentences.push(self.sentence());
                }
                
                if prev_sentences.len() > 5000 {
                    prev_sentences.clear();
                }
            }

            if !find_cycle {
                update_random_char = !update_random_char;
            }
        }
    }

    fn display_progress(thread_epochs: &Arc<Mutex<Vec<AtomicI32>>>, num_threads: usize) {
        if let Ok(epochs) = thread_epochs.lock() {
            print!("\r");
            for i in 0..num_threads {
                let epoch = epochs[i].load(Ordering::Relaxed);
                print!("T{}: {} | ", i + 1, format_with_commas(epoch));
            }
            io::stdout().flush().unwrap();
        }
    }

    pub fn find_counts_and_chars(sentence: &str, include_punctuation: bool) -> Vec<(String, String)> {
        let single_word_numbers: Vec<&str> = WORD_TO_INT.keys().cloned().collect();
        let leading_word_numbers: Vec<&str> = WORD_TO_INT.iter()
            .filter(|(_, &val)| val >= 20)
            .map(|(&key, _)| key)
            .collect();
        
        let leading_word_or = leading_word_numbers.join("|");
        let single_word_or = single_word_numbers.join("|");
        
        let number_re = format!(r"(?P<number>(?:(?:{})[-\s]?)?(?:{}))", leading_word_or, single_word_or);
        
        let punctuation_re = if include_punctuation {
            let punct_words: Vec<&str> = WORD_TO_CHAR.keys()
                .filter(|&&word| !LETTER_CHARS.contains(word))
                .cloned()
                .collect();
            format!("{}|", punct_words.join("|"))
        } else {
            String::new()
        };
        
        let char_re = format!(r"(?P<character>(?:{}[a-z]){{1}})'?(?=s)?s?", punctuation_re);
        let number_char_re = format!(r"\b{}\s{}", number_re, char_re);
        
        let re = Regex::new(&number_char_re).unwrap();
        re.captures_iter(&sentence.to_lowercase())
            .filter_map(|cap| {
                let number = cap.name("number")?.as_str();
                let character = cap.name("character")?.as_str();
                Some((number.to_string(), character.to_string()))
            })
            .collect()
    }
}

pub fn validate_autogram(sentence: &str, include_punctuation: bool, verbose: bool, double_verbose: bool) -> bool {
    let sentence_lower = sentence.to_lowercase();
    let verbose = verbose || double_verbose;
    
    let countable_chars = if include_punctuation {
        format!("{}{}", LETTER_CHARS, PUNCTUATION_CHARS)
    } else {
        LETTER_CHARS.to_string()
    };
    
    let counts: HashMap<char, i32> = countable_chars.chars()
        .filter_map(|ch| {
            let count = sentence_lower.matches(ch).count() as i32;
            if count > 0 { Some((ch, count)) } else { None }
        })
        .collect();

    let counts_and_chars = Autogram::find_counts_and_chars(sentence, include_punctuation);
    
    let mut sentence_counts = HashMap::new();
    for (num_match, char_match) in counts_and_chars.iter() {
        if let (Ok(num), Some(&ch)) = (words_to_num(num_match), WORD_TO_CHAR.get(char_match.as_str())) {
            sentence_counts.insert(ch, num);
        }
    }

    if double_verbose {
        println!("Regex sentence counts: {:?}", counts_and_chars);
        println!("Parsed sentence counts: {:?}", sentence_counts);
        println!("Function counts: {:?}", counts);
    }

    let mut valid = true;
    let mut sentence_counts_copy = sentence_counts.clone();
    
    for (&ch, &count) in &counts {
        if let Some(sc) = sentence_counts_copy.remove(&ch) {
            if count == sc {
                if verbose { println!("{}: {} verified", ch, sc); }
            } else {
                valid = false;
                println!("{}: INVALID. True count: {}, Sentence says: {}.", ch, count, sc);
            }
        } else {
            valid = false;
            println!("{}: Missing from sentence. True count: {}.", ch, count);
        }
    }

    if !sentence_counts_copy.is_empty() {
        panic!("Sentence mentions {} chars that were not found by validate().\n{:?}", 
               sentence_counts_copy.len(), sentence_counts_copy);
    }

    valid
}

pub fn run_validation_tests() {
    let sentences = vec![
        (r#"Spam, Spam, Spam, six a's, two d's, twenty e's, seven f's, four g's,
        five h's, ten i's, two l's, five m's, seven n's, six o's, five p's,
        six r's, thirty-one s's, twelve t's, three u's, eight v's, five w's,
        four x's, three y's, eggs, and Spam."#, false),
        ("twenty e, four f, one g, five h, three i, one l, ten n, seven o, seven r, three s, nine t, three u, four v, three w, one x, two y", false),
        (r#"The output of this Python script is composed of two a's, three c's,
        three d's, thirty-one e's, nine f's, three g's, ten h's, twelve i's,
        two l's, two m's, fourteen n's, fourteen o's, five p's, eight r's,
        twenty-seven s's, twenty-five t's, five u's, eight v's, seven w's,
        one x, and five y's."#, false),
        (r#"This sentence contains three a's, three c's, two d's, twenty-seven e's,
        four f's, one g, five h's, eleven i's, two l's, sixteen n's, seven o's,
        five r's, twenty-nine s's, sixteen t's, two u's, six v's, six w's, six x's,
        and three y's."#, false),
        (r#"The quick brown fox jumped over alphabet soup containing five a's, three b's,
        three c's, three d's, thirty-two e's, six f's, two g's, ten h's, twelve i's,
        two j's, two k's, three l's, two m's, sixteen n's, sixteen o's, four p's,
        two q's, thirteen r's, thirty-four s's, twenty-seven t's, seven u's, seven v's,
        ten w's, six x's, four y's, and one z."#, false),
        (r#"Only the fool would take trouble to verify that his sentence was composed 
        of ten a's, three b's, four c's, four d's, forty-six e's, sixteen f's, 
        four g's, thirteen h's, fifteen i's, two k's, nine l's, four m's, 
        twenty-five n's, twenty-four o's, five p's, sixteen r's, forty-one s's, 
        thirty-seven t's, ten u's, eight v's, eight w's, four x's, eleven y's, 
        twenty-seven commas, twenty-three apostrophes, seven hyphens and, last but 
        not least, a single !"#, true),
    ];

    for (i, (sentence, include_punct)) in sentences.iter().enumerate() {
        println!("\n----------------- sentence {} -----------------", i + 1);
        println!("{}", sentence);
        let is_valid = validate_autogram(sentence, *include_punct, false, false);
        println!("{}", if is_valid { "Valid!" } else { "Invalid!" });
    }
}