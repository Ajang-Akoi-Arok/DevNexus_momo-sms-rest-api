import os
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple, Optional


def extract_tx_id(body: str, fallback_id: str) -> str:
    match = re.search(
        r'(?:TxId:|Financial Transaction Id:)\s*(\d+)',
        body,
        re.IGNORECASE
    )
    return match.group(1) if match else fallback_id


def extract_amount(body: str) -> Optional[float]:
    match = re.search(r'([\d,]+)\s*RWF', body, re.IGNORECASE)

    if match:
        try:
            return float(match.group(1).replace(',', ''))
        except ValueError:
            return None

    return None


def parse_sms_xml(
    file_path: str
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:

    transactions_list: List[Dict[str, Any]] = []
    transactions_dict: Dict[str, Dict[str, Any]] = {}

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for index, elem in enumerate(root.findall(".//sms"), start=1):
            body = elem.attrib.get("body", "")

            fallback_id = f"sms_{index}"
            tx_id = extract_tx_id(body, fallback_id)
            amount = extract_amount(body)

            record = {
                "id": str(tx_id),
                "address": elem.attrib.get("address", ""),
                "date": elem.attrib.get("date", ""),
                "readable_date": elem.attrib.get("readable_date", ""),
                "type": elem.attrib.get("type", ""),
                "amount_rwf": amount,
                "body": body
            }

            transactions_list.append(record)
            transactions_dict[str(tx_id)] = record

        return transactions_list, transactions_dict

    except ET.ParseError as e:
        print(f"[Error] XML Parse Error in {file_path}: {e}")
        return [], {}

    except FileNotFoundError:
        print(
            f"[Error] File not found at path: "
            f"{os.path.abspath(file_path)}"
        )
        return [], {}


if __name__ == "__main__":
    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    xml_path = os.path.join(base_dir, "modified_sms_v2.xml")

    if not os.path.exists(xml_path):
        xml_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "modified_sms_v2.xml"
        )

    data_list, data_dict = parse_sms_xml(xml_path)

    print(f"Parsed {len(data_list)} SMS records.")

    if data_list:
        print("\nFirst Record Preview:")
        print(data_list[0])