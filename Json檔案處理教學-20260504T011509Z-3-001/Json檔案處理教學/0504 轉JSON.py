import FreeCAD
import Import
import os
import pandas as pd
import json


class CADFeatureExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.shape = self._load_shape()

    def _load_shape(self):
        """讀取模型並回傳 Shape 物件"""
        Import.open(self.file_path)
        doc = FreeCAD.ActiveDocument
        part_obj = next((obj for obj in doc.Objects if hasattr(obj, 'Shape')), None)

        if not part_obj:
            FreeCAD.closeDocument(doc.Name)
            return None

        shape_copy = part_obj.Shape.copy()
        FreeCAD.closeDocument(doc.Name)
        return shape_copy

    def extract_features(self):
        """提取特徵並回傳字典"""
        if not self.shape:
            return None

        s = self.shape
        bbox = s.BoundBox

        return {
            "FileName": self.file_name,
            "Volume": s.Volume,
            "Area": s.Area,
            "Faces_Count": len(s.Faces),
            "Edges_Count": len(s.Edges),
            "BBox_X": bbox.XMax - bbox.XMin,
            "BBox_Y": bbox.YMax - bbox.YMin,
            "BBox_Z": bbox.ZMax - bbox.ZMin,
            "Center_X": s.CenterOfMass.x,
            "Center_Y": s.CenterOfMass.y,
            "Center_Z": s.CenterOfMass.z

        }




def run_batch_analysis(folder_path):
    all_results = []


    for file in os.listdir(folder_path):
        if file.lower().endswith(('.step', '.stp')):
            full_path = os.path.join(folder_path, file)
            print(f"正在處理: {file}...")

            try:
                # 使用 OOP 類別
                extractor = CADFeatureExtractor(full_path)
                data = extractor.extract_features()

                if data:
                    all_results.append(data)
            except Exception as e:
                print(f"檔案 {file} 處理失敗: {e}")


    if not all_results:
        print("沒有找到任何 STEP 檔案或資料提取失敗。")
        return None


    csv_filename = "cad_features_analysis.csv"
    df = pd.DataFrame(all_results)
    df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

    # 3. 將字典列表直接輸出為 JSON
    json_filename = "cad_features_analysis.json"
    with open(json_filename, 'w', encoding='utf-8') as f:

        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print(f" 分析完成！共處理 {len(df)} 個檔案。")
    print(f"結果已分別存至: {csv_filename} 與 {json_filename}")

    return df



target_folder = r"C:\0427\毛胚-20260427T022116Z-3-001\毛胚"
result_df = run_batch_analysis(target_folder)