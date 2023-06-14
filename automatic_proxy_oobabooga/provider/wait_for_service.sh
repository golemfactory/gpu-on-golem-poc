#! /bin/bash

while ! curl -s http://localhost:"$1"/api/v1/generate --data '{"prompt": "I am happy prompt and I", , "max_new_tokens, ": 5, , "do_sample, ": True, , "temperature, ": 1.3, , "top_p, ": 0.1, , "typical_p, ": 1, , "epsilon_cutoff, ": 0, , "eta_cutoff, ": 0, , "tfs, ": 1, , "top_a, ": 0, , "repetition_penalty, ": 1.18, , "top_k, ": 40, , "min_length, ": 0, , "no_repeat_ngram_size, ": 0, , "num_beams, ": 1, , "penalty_alpha, ": 0, , "length_penalty, ": 1, , "early_stopping, ": False, , "mirostat_mode, ": 0, , "mirostat_tau, ": 5, , "mirostat_eta, ": 0.1, , "seed, ": -1, , "add_bos_token, ": True, , "truncation_length, ": 2048, , "ban_eos_token, ": False, , "skip_special_tokens, ": True, , "stopping_strings, ": []}' > /dev/null
do
    echo waiting for service
    sleep 1
done
echo Service worked
