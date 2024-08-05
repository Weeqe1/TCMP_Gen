from itertools import combinations
import numpy as np
import pandas as pd

def apri(transactions, min_support):
    itemsets = {}
    frequent_itemsets = {}
    candidates = []

    for transaction in transactions:
        for item in transaction:
            if item not in itemsets:
                itemsets[item] = 1
            else:
                itemsets[item] += 1

    for item, count in itemsets.items():
        support = float(count) / len(transactions)
        if support >= min_support:
            temp = (item,)
            frequent_itemsets[temp] = support
            candidates.append([item])

    k = 2
    while candidates:
        itemsets = generate_itemsets(candidates, k)
        candidates = []
        for itemset in itemsets:
            support = calculate_support(itemset, transactions)
            if support >= min_support:
                frequent_itemsets[tuple(sorted(itemset))] = support
                candidates.append(itemset)
        k += 1

    return frequent_itemsets

def generate_itemsets(candidates, k):
    itemsets = []
    num_candidates = len(candidates)

    for i in range(num_candidates):
        for j in range(i + 1, num_candidates):
            itemset1 = candidates[i][:k - 2]
            itemset2 = candidates[j][:k - 2]
            if itemset1 == itemset2:
                itemsets.append(candidates[i] + [candidates[j][k - 2]])

    return itemsets

def calculate_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return float(count) / len(transactions)

def delete_dict(arr, dic):
    print("ARR IS ",arr)
    for key in list(dic.keys()):
        if any(item in key for item in arr):
            del dic[key]

    return dic

def association_rules(df, min_threshold,metric="confidence",  support_only=False):

    if not df.shape[0]:
        raise ValueError(
            "The input DataFrame `df` containing " "the frequent itemsets is empty."
        )

    if not all(col in df.columns for col in ["support", "itemsets"]):
        raise ValueError(
            "Dataframe needs to contain the\
                         columns 'support' and 'itemsets'"
        )

    def conviction_helper(AC, A, C):
        confidence = AC / A
        conviction = np.empty(confidence.shape, dtype=float)
        if not len(conviction.shape):
            conviction = conviction[np.newaxis]
            confidence = confidence[np.newaxis]
            AC = AC[np.newaxis]
            A = A[np.newaxis]
            C = C[np.newaxis]
        conviction[:] = np.inf
        conviction[confidence < 1.0] = (1.0 - C[confidence < 1.0]) / (
            1.0 - confidence[confidence < 1.0]
        )

        return conviction

    metric_dict = {
        "antecedent support": lambda _, A, __: A,
        "consequent support": lambda _, __, C: C,
        "support": lambda AC, _, __: AC,
        "confidence": lambda AC, sA, _: AC / sA,
    }

    columns_ordered = [
        "antecedent support",
        "consequent support",
        "support",
        "confidence",
    ]

    if support_only:
        metric = "support"
    else:
        if metric not in metric_dict.keys():
            raise ValueError(
                "Metric must be 'confidence' or 'lift', got '{}'".format(metric)
            )

    keys = df["itemsets"].values
    values = df["support"].values
    frozenset_vect = np.vectorize(lambda x: frozenset(x))
    frequent_items_dict = dict(zip(frozenset_vect(keys), values))

    rule_antecedents = []
    rule_consequents = []
    rule_supports = []

    for k in frequent_items_dict.keys():
        AC = frequent_items_dict[k]
        for idx in range(len(k) - 1, 0, -1):
            for c in combinations(k, r=idx):
                antecedent = frozenset(c)
                consequent = k.difference(antecedent)

                if support_only:
                    A = None
                    C = None

                else:
                    try:
                        A = frequent_items_dict[antecedent]
                        C = frequent_items_dict[consequent]
                    except KeyError as e:
                        s = (
                            str(e) + "This error indicates a missing Dataframe antecedent or trailing word Try using "
                                     "the 'support_only=True' option "
                        )
                        raise KeyError(s)

                score = metric_dict[metric](AC, A, C)
                if score >= min_threshold:
                    rule_antecedents.append(antecedent)
                    rule_consequents.append(consequent)
                    rule_supports.append([AC, A, C])

    if not rule_supports:
        return pd.DataFrame(columns=["antecedents", "consequents"] + columns_ordered)

    else:
        rule_supports = np.array(rule_supports).T.astype(float)
        df_res = pd.DataFrame(
            data=list(zip(rule_antecedents, rule_consequents)),
            columns=["antecedents", "consequents"],
        )

        if support_only:
            AC = rule_supports[0]
            for m in columns_ordered:
                df_res[m] = np.nan
            df_res["support"] = AC

        else:
            AC = rule_supports[0]
            A = rule_supports[1]
            C = rule_supports[2]
            for m in columns_ordered:
                df_res[m] = metric_dict[m](AC, A, C)

        def frozenset_to_str(f):
            return ",".join(sorted(f)) if isinstance(f, frozenset) else f

        dfx = df_res.applymap(frozenset_to_str)
        return dfx

def association_filtered(df,an_min_support,cons_min_support):
        filtered_df = df[
            (df['antecedent support'] >= an_min_support) & (df['consequent support'] >= cons_min_support)]
        sorted_df = filtered_df.sort_values(['antecedent support', 'consequent support'], ascending=[False, False])

        return sorted_df