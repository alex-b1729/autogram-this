use clap::Parser;
use autogramthis::{Autogram, validate_autogram};

#[derive(Parser)]
#[command(name = "autogramthis")]
#[command(about = "Search for autograms from an optional starting or ending string or validate an autogram")]
struct Args {
    /// The text to begin the autogram sentence
    prefix: Option<String>,

    /// The text to end the autogram sentence
    #[arg(short, long, default_value = "")]
    suffix: String,

    /// Search for a pangram - i.e. where every letter occurs at least once
    #[arg(short, long)]
    pangram: bool,

    /// Exclude the 's from characters with count greater than one
    #[arg(long)]
    make_singular: bool,

    /// Exclude the word 'and' from before the last character's count
    #[arg(long)]
    no_and: bool,

    /// Include the punctuation characters in search and validation
    #[arg(long)]
    include_punctuation: bool,

    /// Validate whether the given string is an autogram
    #[arg(long)]
    validate: Option<String>,

    /// Verbose output when validating
    #[arg(short, long)]
    verbose: bool,

    /// Find cycles instead of autograms
    #[arg(long)]
    find_cycle: bool,

    /// Use single-threaded search instead of parallel
    #[arg(long)]
    single_thread: bool,
}

fn main() {
    let args = Args::parse();

    if let Some(sentence) = args.validate {
        let is_valid = validate_autogram(&sentence, args.include_punctuation, args.verbose, false);
        println!("{}", if is_valid { "Valid autogram!" } else { "Invalid!" });
    } else {
        let prefix = args.prefix.unwrap_or_default();
        let mut ag = Autogram::new(&prefix, &args.suffix);
        ag.make_plural = !args.make_singular;
        ag.include_final_and = !args.no_and;
        ag.is_pangram = args.pangram;
        ag.include_punctuation = args.include_punctuation;
        
        if args.single_thread {
            ag.search(args.find_cycle);
        } else {
            ag.search_parallel(args.find_cycle);
        }
    }
}