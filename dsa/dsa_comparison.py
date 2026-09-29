import time
from typing import List, Dict, Any, Optional

from parse_xml import parse_sms_xml


def linear_search(
    transactions: List[Dict[str, Any]],
    target_id: str
) -> Optional[Dict[str, Any]]:
    for record in transactions:
        if record.get("id") == target_id:
            return record
    return None


def dictionary_lookup(
    transactions_map: Dict[str, Dict[str, Any]],
    target_id: str
) -> Optional[Dict[str, Any]]:
    return transactions_map.get(target_id)


def compare_search_performance(
    transactions_list: List[Dict[str, Any]],
    transactions_dict: Dict[str, Dict[str, Any]],
    target_id: str,
    iterations: int = 100000
) -> Dict[str, Any]:

    start = time.perf_counter()

    for _ in range(iterations):
        linear_search(transactions_list, target_id)

    linear_time = time.perf_counter() - start

    start = time.perf_counter()

    for _ in range(iterations):
        dictionary_lookup(transactions_dict, target_id)

    dictionary_time = time.perf_counter() - start

    speedup = (
        linear_time / dictionary_time
        if dictionary_time > 0
        else 0
    )

    return {
        "target_id": target_id,
        "total_records": len(transactions_list),
        "iterations": iterations,
        "linear_search_time_sec": round(linear_time, 6),
        "dict_lookup_time_sec": round(dictionary_time, 6),
        "speedup_factor": round(speedup, 2)
    }


if __name__ == "__main__":
    xml_path = "modified_sms_v2.xml"

    transactions, transactions_dict = parse_sms_xml(xml_path)

    if len(transactions) >= 20:
        test_records = transactions[:20]

        test_dict = {
            record["id"]: record
            for record in test_records
        }

        target_id = test_records[-1]["id"]

        results = compare_search_performance(
            test_records,
            test_dict,
            target_id
        )

        print("DSA SEARCH COMPARISON")
        print("---------------------")
        print(f"Records tested: {results['total_records']}")
        print(f"Target ID: {results['target_id']}")
        print(f"Iterations: {results['iterations']:,}")
        print(
            f"Linear Search Time: "
            f"{results['linear_search_time_sec']} seconds"
        )
        print(
            f"Dictionary Lookup Time: "
            f"{results['dict_lookup_time_sec']} seconds"
        )
        print(
            f"Dictionary Speedup: "
            f"{results['speedup_factor']}x"
        )
        print()
        print("Linear Search: O(n)")
        print("Dictionary Lookup: O(1) average case")
        print("Binary Search on sorted data: O(log n)")
    else:
        print("At least 20 records are required for the comparison.")