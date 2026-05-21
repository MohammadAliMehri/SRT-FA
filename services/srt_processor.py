import concurrent.futures
import re
from services.translator import translate_block
from services.persian_utils import polish_persian
from services.subtitle_formatter import format_subtitle

BATCH_SIZE = 50 # Number of subtitle blocks per request
MAX_THREADS = 5   # Reduced for lower resource usage

def process_batch(batch_blocks):
    """
    Processes a batch of blocks in a single translation request.
    """
    if not batch_blocks:
        return []

    # Prepare indices and original texts
    indices = [b[0] for b in batch_blocks]
    timecodes = [b[1] for b in batch_blocks]
    original_texts = [" ".join(b[2:]) for b in batch_blocks]

    # Join with a unique separator that is likely preserved
    separator = " @@@ "
    combined_text = separator.join(original_texts)

    # Translate the entire batch
    translated_combined = translate_block(combined_text)
    
    # Split back - using regex to be resilient to whitespace around separator
    translated_parts = re.split(r'\s*@@@\s*', translated_combined)
    
    # Filter out empty or whitespace-only strings
    translated_parts = [p.strip() for p in translated_parts if p.strip()]

    results = []
    if len(translated_parts) != len(batch_blocks):
        # Fallback to individual blocks if batch split count mismatch
        for i in range(len(batch_blocks)):
            idx = indices[i]
            tc = timecodes[i]
            translated = translate_block(original_texts[i])
            processed = polish_persian(translated)
            formatted = format_subtitle(processed)
            results.append((int(idx), "\n".join([str(idx), tc, formatted])))
    else:
        for i in range(len(batch_blocks)):
            idx = indices[i]
            tc = timecodes[i]
            translated = translated_parts[i]
            processed = polish_persian(translated)
            formatted = format_subtitle(processed)
            results.append((int(idx), "\n".join([str(idx), tc, formatted])))
    
    return results

def process_blocks(blocks, progress_callback):
    """
    Translates blocks in parallel using a thread pool with batching.
    """
    results = []
    total_blocks = len(blocks)
    
    # Create batches
    batches = [blocks[i:i + BATCH_SIZE] for i in range(0, len(blocks), BATCH_SIZE)]
    completed_blocks = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_batch = {executor.submit(process_batch, batch): batch for batch in batches}
        
        for future in concurrent.futures.as_completed(future_to_batch):
            try:
                batch_results = future.result()
                results.extend(batch_results)
                
                completed_blocks += len(batch_results)
                if total_blocks > 0:
                    progress = int((completed_blocks / total_blocks) * 100)
                    progress_callback(progress)
            except Exception as e:
                print(f"Error processing batch: {e}")

    results.sort(key=lambda x: x[0])
    final_output = [r[1] for r in results]

    return "\n\n".join(final_output)
