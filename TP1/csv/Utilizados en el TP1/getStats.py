import csv
import os

def extract_stats(input_filename: str, output_filename: str) -> None:
    """
    Reads a CSV file and creates a new CSV with 'gen', 'min', 'avg', 'max', and 'mejor_cromosoma' columns.
    
    Args:
        input_filename (str): Path to the input CSV file.
        output_filename (str): Path to the output CSV file.
    """
    try:
        # Dictionary to store stats per generation
        stats = {}
        
        # Read the input CSV
        with open(input_filename, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                try:
                    gen = int(row['gen'])
                    if gen not in stats:  # Only take the first row for each generation
                        # Determine the best chromosome column name ('mejor_cromosoma' or 'mejor')
                        best_chrom_key = 'mejor_cromosoma' if 'mejor_cromosoma' in row else 'mejor'
                        stats[gen] = {
                            'min': float(row['min']),
                            'avg': float(row['avg']),
                            'max': float(row['max']),
                            'mejor_cromosoma': row[best_chrom_key]
                        }
                except (KeyError, ValueError) as e:
                    print(f"Error processing row in {input_filename}: {e}")
                    continue
        
        # Write to output CSV
        with open(output_filename, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['gen', 'min', 'avg', 'max', 'mejor_cromosoma'])  # Write header
            for gen in sorted(stats.keys()):
                writer.writerow([
                    gen,
                    stats[gen]['min'],
                    stats[gen]['avg'],
                    stats[gen]['max'],
                    stats[gen]['mejor_cromosoma']
                ])
        print(f"Successfully generated {output_filename}")
    except FileNotFoundError:
        print(f"Input file {input_filename} not found")
    except Exception as e:
        print(f"Error processing {input_filename}: {e}")

def process_folders(folders: list[str], input_files: list[str]) -> None:
    """
    Iteratively processes CSV files in specified folders to generate stats CSVs.
    
    Args:
        folders (list[str]): List of folder names ('20', '100', '200').
        input_files (list[str]): List of input CSV filenames.
    """
    for folder in folders:
        for input_file in input_files:
            input_path = os.path.join(folder, input_file)
            output_file = input_file.replace('.csv', '_stats.csv')
            output_path = os.path.join(folder, output_file)
            if os.path.exists(input_path):
                extract_stats(input_path, output_path)
            else:
                print(f"File {input_path} does not exist")

if __name__ == "__main__":
    folders = ['20', '100', '200']
    input_files = [
        'poblacion_ruleta.csv',
        'poblacion_elitismo.csv',
        'poblacion_torneo.csv'
    ]
    process_folders(folders, input_files)