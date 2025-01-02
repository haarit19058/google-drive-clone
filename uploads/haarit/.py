#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 12:15:57 2021

@author: akshat
"""
from typing import Dict
import random
import multiprocessing

import rdkit
from rdkit import Chem

import selfies 
from selfies import encoder, decoder

from .utils import get_selfies_chars

def mutate_sf(sf_chars, alphabet, num_sample_frags, base_alphabet = None):
    """
    Given a list of SELFIES alphabets, make random changes to the molecule using 
    alphabet. Opertations to molecules are character replacements, additions and deletions. 

    Parameters
    ----------
    sf_chars : (list of string alphabets)
        List of string alphabets for a SELFIE string.
    alphabet : (list of SELFIE strings)
        New SELFIES characters are added here and sampled.
    num_sample_frags: (int)
        Number of randomly sampled SELFIE strings.
    base_alphabet: (list of SELFIE strings)
        Main alphabet that will be appended with the introduced characters above.
        If none, use the semantic robust alphabet.

    Returns
    -------
    Mutated SELFIE string.

    """
    if base_alphabet is None:
        base_alphabet = list(selfies.get_semantic_robust_alphabet())
    random_char_idx = random.choice(range(len(sf_chars)))
    choices_ls = [1, 2, 3]  # 1 = replacement; 2 = addition; 3=delete
    mutn_choice = choices_ls[
        random.choice(range(len(choices_ls)))
    ]  # Which mutation to do:

    if alphabet != []:
        alphabet = random.sample(alphabet, num_sample_frags) + base_alphabet
    else:
        alphabet = base_alphabet

    # Mutate character:
    if mutn_choice == 1:
        random_char = alphabet[random.choice(range(len(alphabet)))]
        change_sf = (
            sf_chars[0:random_char_idx]
            + [random_char]
            + sf_chars[random_char_idx + 1 :]
        )

    # add character:
    elif mutn_choice == 2:
        random_char = alphabet[random.choice(range(len(alphabet)))]
        change_sf = (
            sf_chars[0:random_char_idx] + [random_char] + sf_chars[random_char_idx:]
        )

    # delete character:
    elif mutn_choice == 3:
        if len(sf_chars) != 1:
            change_sf = sf_chars[0:random_char_idx] + sf_chars[random_char_idx + 1 :]
        else:
            change_sf = sf_chars

    return "".join(x for x in change_sf)


def mutate_smiles(
    smile, alphabet, num_random_samples, num_mutations, num_sample_frags, base_alphabet = None
):
    """
    Given an input smile, perform mutations to the strucutre using provided SELFIE
    alphabet list. 'num_random_samples' number of different SMILES orientations are 
    considered & total 'num_mutations' are performed. 

    Parameters
    ----------
    smile : (str)
        Valid SMILES string.
    alphabet : (list of str)
        list of SELFIE strings.
    num_random_samples : (int)
        Number of different SMILES orientations to be formed for the input smile.
    num_mutations : TYPE
        Number of mutations to perform on each of different orientations SMILES.
    num_sample_frags: (int)
        Number of randomly sampled SELFIE strings.

    Returns
    -------
    mutated_smiles_canon : (list of strings)
        List of unique molecules produced from mutations.
    """
    mol = Chem.MolFromSmiles(smile)
    Chem.Kekulize(mol)

    # Obtain randomized orderings of the SMILES:
    randomized_smile_orderings = []
    for _ in range(num_random_samples):
        randomized_smile_orderings.append(
            rdkit.Chem.MolToSmiles(
                mol,
                canonical=False,
                doRandom=True,
                isomericSmiles=False,
                kekuleSmiles=True,
            )
        )

    # Convert all the molecules to SELFIES
    selfies_ls = [encoder(x) for x in randomized_smile_orderings]
    selfies_ls_chars = [get_selfies_chars(selfie) for selfie in selfies_ls]

    # Obtain the mutated selfies
    mutated_sf = []
    for sf_chars in selfies_ls_chars:

        for i in range(num_mutations):
            if i == 0:
                mutated_sf.append(mutate_sf(sf_chars, alphabet, num_sample_frags, base_alphabet))
            else:
                mutated_sf.append(
                    mutate_sf(
                        get_selfies_chars(mutated_sf[-1]), alphabet, num_sample_frags, base_alphabet
                    )
                )

    mutated_smiles = [decoder(x) for x in mutated_sf]
    mutated_smiles_canon = []
    for item in mutated_smiles:
        try:
            smi_canon = Chem.MolToSmiles(
                Chem.MolFromSmiles(item, sanitize=True),
                isomericSmiles=False,
                canonical=True,
            )
            if smi_canon != "": 
                mutated_smiles_canon.append(smi_canon)
        except:
            continue

    mutated_smiles_canon = list(set(mutated_smiles_canon))
    return mutated_smiles_canon



if __name__ == "__main__":
    molecules_here = [
        "CCC",
        "CCCC",
        "CCCCC",
        "CCCCCCCC",
        "CS",
        "CSSS",
        "CSSSSS",
        "CF",
        "CI",
        "CBr",
        "CSSSSSSSSSSSS",
        "CSSSSSSSSSC",
        "CSSSSCCSSSC",
        "CSSSSSSSSSF",
        "SSSSSC",
    ]
    A = get_mutated_smiles(
        molecules_here, alphabet=["[C]"] * 500, num_sample_frags=200, space="Explore"
    )

list = smi_list * num_random_samples
        with multiprocessing.Pool(self.num_workers) as pool:
            mut_smi_list = pool.map(
                partial(
                    mutate_smiles,
                    alphabet=self.frag_alphabet,
                    num_random_samples=1,
                    num_mutations=num_mutations,
                    num_sample_frags=self.num_sample_frags,
                    base_alphabet=self.alphabet
                ),
                smi_list,
            )
        mut_smi_list = self.flatten_list(mut_smi_list)
        return mut_smi_list

    def crossover_smi_list(self, smi_list: List[str]):
        # parallelized crossover function
        with multiprocessing.Pool(self.num_workers) as pool:
            cross_smi = pool.map(
                partial(
                    crossover_smiles,
                    crossover_num_random_samples=self.crossover_num_random_samples,
                ),
                smi_list,
            )
        cross_smi = self.flatten_list(cross_smi)
        return cross_smi

    def check_filters(self, smi_list: List[str]):
        if self.custom_filter is not None:
            smi_list = [smi for smi in smi_list if self.custom_filter(smi)]
        return smi_list

    def save_hyperparameters(self):
        hparams = {
            k: v if not callable(v) else v.__name__ for k, v in vars(self).items()
        }
        with open(os.path.join(self.work_dir, "hparams.yml"), "w") as f:
            yaml.dump(hparams, f)

    def run(self):
        """ Run optimization based on hyperparameters initialized
        """

        for gen_ in range(self.generations):

            # bookkeeping
            if self.verbose_out:
                output_dir = os.path.join(self.work_dir, f"{gen_}_DATA")
                if not os.path.isdir(output_dir):
                    os.mkdir(output_dir)

            print(f"On generation {gen_}/{self.generations}")

            keep_smiles, replace_smiles = self.get_good_bad_smiles(
                self.fitness, self.population, self.generation_size
            )
            replace_smiles = list(set(replace_smiles))

            ### EXPLORATION ###
            # Mutate and crossover (with keep_smiles) molecules that are meant to be replaced
            explr_smiles = []
            timeout_counter = 0
            while len(explr_smiles) < self.generation_size-len(keep_smiles):
                # Mutations:
                mut_smi_explr = self.mutate_smi_list(
                    replace_smiles[0 : len(replace_smiles) // 2], space="explore"
                )
                mut_smi_explr = self.check_filters(mut_smi_explr)

                # Crossovers:
                smiles_join = []
                for item in replace_smiles[len(replace_smiles) // 2 :]:
                    smiles_join.append(item + "xxx" + random.choice(keep_smiles))
                cross_smi_explr = self.crossover_smi_list(smiles_join)
                cross_smi_explr = self.check_filters(cross_smi_explr)

                # Combine and get unique smiles not yet found
                all_smiles = list(set(mut_smi_explr + cross_smi_explr))
                for x in all_smiles:
                    if x not in self.smiles_collector:
                        explr_smiles.append(x)
                explr_smiles = list(set(explr_smiles))

                timeout_counter += 1
                if timeout_counter % 100 == 0:
                    print(f'Exploration: {timeout_counter} iterations of filtering. \
                    Filter may be too strict, or you need more mutations/crossovers.')

            # Replace the molecules with ones in exploration mutation/crossover
            if not self.use_classifier or gen_ == 0:
                replaced_pop = random.sample(
                    explr_smiles, self.generation_size - len(keep_smiles)
                )
            else:
                # The sampling needs to be done by the neural network!
                print("    Training classifier neural net...")
                train_smiles, targets = [], []
                for item in self.smiles_collector:
                    train_smiles.append(item)
                    targets.append(self.smiles_collector[item][0])
                net = create_and_train_network(
                    train_smiles,
                    targets,
                    num_workers=self.num_workers,
                    use_gpu=self.use_gpu,
                )

                # Obtain predictions on unseen molecules:
                print("    Obtaining Predictions")
                new_predictions = obtain_model_pred(
                    explr_smiles,
                    net,
                    num_workers=self.num_workers,
                    use_gpu=self.use_gpu,
                )
                sorted_idx = np.argsort(np.squeeze(new_predictions))[::-1]
                replaced_pop = np.array(explr_smiles)[
                    sorted_idx[: self.generation_size - len(keep_smiles)]
                ].tolist()

            # Calculate actual fitness for the exploration population
            self.population = keep_smiles + replaced_pop
            self.fitness = []
            for smi in self.population:
                if smi in self.smiles_collector:
                    # if already calculated, use the value from smiles collector
                    self.fitness.append(self.smiles_collector[smi][0])
                    self.smiles_collector[smi][1] += 1
                else:
                    # make a calculation
                    f = self.fitness_function(smi)
                    self.fitness.append(f)
                    self.smiles_collector[smi] = [f, 1]

            # Print exploration data
            idx_sort = np.argsort(self.fitness)[::-1]
            print(f"    (Explr) Top Fitness: {self.fitness[idx_sort[0]]}")
            print(f"    (Explr) Top Smile: {self.population[idx_sort[0]]}")

            fitness_sort = np.array(self.fitness)[idx_sort]
            if self.verbose_out:
                with open(
                    os.path.join(
                        self.work_dir, str(gen_) + "_DATA", "fitness_explore.txt"
                    ),
                    "w",
                ) as f:
                    f.writelines(["{} ".format(x) for x in fitness_sort])
                    f.writelines(["\n"])
            else:
                with open(os.path.join(self.work_dir, "fitness_explore.txt"), "w") as f:
                    f.writelines(["{} ".format(x) for x in fitness_sort])
                    f.writelines(["\n"])

            # this population is sort by modified fitness, if active
            population_sort = np.array(self.population)[idx_sort]
            if self.verbose_out:
                with open(
                    os.path.join(
                        self.work_dir, str(gen_) + "_DATA", "population_explore.txt"
                    ),
                    "w",
                ) as f:
                    f.writelines(["{} ".format(x) for x in population_sort])
                    f.writelines(["\n"])
            else:
                with open(
                    os.path.join(self.work_dir, "population_explore.txt"), "w"
                ) as f:
                    f.writelines(["{} ".format(x) for x in population_sort])
                    f.writelines(["\n"])

            ### EXPLOITATION ###
            # Conduct local search on top-n molecules from population, mutate and do similarity search
            exploit_smiles = []
            timeout_counter = 0
            while len(exploit_smiles) < self.generation_size:
                smiles_local_search = population_sort[0 : self.top_mols].tolist()
                mut_smi_loc = self.mutate_smi_list(smiles_local_search, "local")
                mut_smi_loc = self.check_filters(mut_smi_loc)

                # filter out molecules already found
                for x in mut_smi_loc:
                    if x not in self.smiles_collector:
                        exploit_smiles.append(x)

                timeout_counter += 1
                if timeout_counter % 100 == 0:
                    print(f'Exploitation: {timeout_counter} iterations of filtering. \
                    Filter may be too strict, or you need more mutations/crossovers.')

            # sort by similarity, only keep ones similar to best
            fp_scores = get_fp_scores(exploit_smiles, population_sort[0])
            fp_sort_idx = np.argsort(fp_scores)[::-1][: self.generation_size]
            # highest fp_score idxs
            self.population_loc = np.array(exploit_smiles)[
                fp_sort_idx
            ]  # list of smiles with highest fp scores

            # STEP 4: CALCULATE THE FITNESS FOR THE LOCAL SEARCH:
            # Exploitation data generated from similarity search is measured with fitness function
            self.fitness_loc = []
            for smi in self.population_loc:
                f = self.fitness_function(smi)
                self.fitness_loc.append(f)
                self.smiles_collector[smi] = [f, 1]

            # List of original local fitness scores
            idx_sort = np.argsort(self.fitness_loc)[
                ::-1
            ]  # index of highest to lowest fitness scores
            print(f"    (Local) Top Fitness: {self.fitness_loc[idx_sort[0]]}")
            print(f"    (Local) Top Smile: {self.population_loc[idx_sort[0]]}")

            fitness_sort = np.array(self.fitness_loc)[idx_sort]
            if self.verbose_out:
                with open(
                    os.path.join(
                        self.work_dir, str(gen_) + "_DATA", "fitness_local_search.txt"
                    ),
                    "w",
                ) as f:
                    f.writelines(["{} ".format(x) for x in fitness_sort])
                    f.writelines(["\n"])
            else:
                with open(
                    os.path.join(self.work_dir, "fitness_local_search.txt"), "w"
                ) as f:
                    f.writelines(["{} ".format(x) for x in fitness_sort])
                    f.writelines(["\n"])

            population_sort = np.array(self.population_loc)[idx_sort]
            if self.verbose_out:
                with open(
                    os.path.join(
                        self.work_dir,
                        str(gen_) + "_DATA",
                        "population_local_search.txt",
                    ),
                    "w",
                ) as f:
                    f.writelines(["{} ".format(x) for x in population_sort])
                    f.writelines(["\n"])
            else:
                with open(
                    os.path.join(self.work_dir, "population_local_search.txt"), "w"
                ) as f:
                    f.writelines(["{} ".format(x) for x in population_sort])
                    f.writelines(["\n"])

            # STEP 5: EXCHANGE THE POPULATIONS:
            # Introduce changes to 'fitness' & 'population'
            best_smi_local = population_sort[0 : self.num_exchanges]
            best_fitness_local = fitness_sort[0 : self.num_exchanges]

            # But will print the best fitness values in file
            idx_sort = np.argsort(self.fitness)[
                ::-1
            ]  # sorted indices for the entire population
            worst_indices = idx_sort[
                -self.num_exchanges :
            ]  # replace worst ones with the best ones
            for i, idx in enumerate(worst_indices):
                try:
                    self.population[idx] = best_smi_local[i]
                    self.fitness[idx] = best_fitness_local[i]
                except:
                    continue

            # Save best of generation!:
            fit_all_best = np.argmax(self.fitness)

            # write best molecule with best fitness
            with open(
                os.path.join(self.work_dir, "generation_all_best.txt"), "a+"
            ) as f:
                f.writelines(
                    f"Gen:{gen_}, {self.population[fit_all_best]}, {self.fitness[fit_all_best]} \n"
                )

        return

    @staticmethod
    def get_good_bad_smiles(fitness, population, generation_size):
        """
        Given fitness values of all SMILES in population, and the generation size, 
        this function smplits  the population into two lists: keep_smiles & replace_smiles. 
        
        Parameters
        ----------
        fitness : (list of floats)
            List of floats representing properties for molecules in population.
        population : (list of SMILES)
            List of all SMILES in each generation.
        generation_size : (int)
            Number of molecules in each generation.

        Returns
        -------
        keep_smiles : (list of SMILES)
            A list of SMILES that will be untouched for the next generation. .
        replace_smiles : (list of SMILES)
            A list of SMILES that will be mutated/crossed-oved for forming the subsequent generation.

        """

        fitness = np.array(fitness)
        idx_sort = fitness.argsort()[::-1]  # Best -> Worst
        keep_ratio = 0.2
        keep_idx = int(len(list(idx_sort)) * keep_ratio)
        try:

            F_50_val = fitness[idx_sort[keep_idx]]
            F_25_val = np.array(fitness) - F_50_val
            F_25_val = np.array([x for x in F_25_val if x < 0]) + F_50_val
            F_25_sort = F_25_val.argsort()[::-1]
            F_25_val = F_25_val[F_25_sort[0]]

            prob_ = 1.0 / (3.0 ** ((F_50_val - fitness) / (F_50_val - F_25_val)) + 1)

            prob_ = prob_ / sum(prob_)
            to_keep = np.random.choice(generation_size, keep_idx, p=prob_)
            to_replace = [i for i in range(generation_size) if i not in to_keep][
                0 : generation_size - len(to_keep)
            ]

            keep_smiles = [population[i] for i in to_keep]
            replace_smiles = [population[i] for i in to_replace]

            best_smi = population[idx_sort[0]]
            if best_smi not in keep_smiles:
                keep_smiles.append(best_smi)
                if best_smi in replace_smiles:
                    replace_smiles.remove(best_smi)

            if keep_smiles == [] or replace_smiles == []:
                raise Exception("Badly sampled population!")
        except:
            keep_smiles = [population[i] for i in idx_sort[:keep_idx]]
            replace_smiles = [population[i] for i in idx_sort[keep_idx:]]

        return keep_smiles, replace_smiles

    def log(self):
        pass

    @staticmethod
    def flatten_list(nested_list):
        return [item for sublist in nested_list for item in sublist]

