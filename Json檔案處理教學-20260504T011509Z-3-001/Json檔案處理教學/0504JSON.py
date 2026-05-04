import FreeCAD
import Import
import json  # 新增 json 模組來處理輸出
from ifcopenshell.util import shape

def extract_basic_geometry(file_path):
    # 1. 載入 STEP 檔案
    Import.open(file_path)
    doc = FreeCAD.ActiveDocument

    # 2. 取得模型中的 Shape 物件
    part_obj = next((obj for obj in doc.Objects if hasattr(obj, 'Shape')), None)
    if not part_obj:
        return None

    shape = part_obj.Shape

    # 3. 提取幾何參數
    geometry_data = {
        "Volume": shape.Volume,
        "Area": shape.Area,
        "Faces_Count": len(shape.Faces),
        "Edges_Count": len(shape.Edges),
        "centerofmass_x": shape.CenterOfMass.x,
        "centerofmass_y": shape.CenterOfMass.y,
        "centerofmass_z": shape.CenterOfMass.z,

        # Bounding Box 的長寬高
        "BoundingBox_XMAX": shape.BoundBox.XMax,
        "BoundingBox_YMAX": shape.BoundBox.YMax,
        "BoundingBox_ZMAX": shape.BoundBox.ZMax,
        "BoundingBox_XMIN": shape.BoundBox.XMin,
        "BoundingBox_YMIN": shape.BoundBox.YMin,
        "BoundingBox_ZMIN": shape.BoundBox.ZMin,
        "BoundingBox_Length_x": shape.BoundBox.XMax - shape.BoundBox.XMin,
        "BoundingBox_Length_y": shape.BoundBox.YMax - shape.BoundBox.YMin,
        "BoundingBox_Length_z": shape.BoundBox.ZMax - shape.BoundBox.ZMin,

        "MomentofIntertia_A11": shape.MatrixOfInertia.A11,
        "MomentofIntertia_A12": shape.MatrixOfInertia.A12,
        "MomentofIntertia_A13": shape.MatrixOfInertia.A13,
        "MomentofIntertia_A21": shape.MatrixOfInertia.A21,
        "MomentofIntertiaA22": shape.MatrixOfInertia.A22,
        "MomentofIntertiaA23": shape.MatrixOfInertia.A23,
        "MomentofIntertiaA31": shape.MatrixOfInertia.A31,
        "MomentofIntertiaA32": shape.MatrixOfInertia.A32,
        "MomentofIntertiaA33": shape.MatrixOfInertia.A33,
    }

    FreeCAD.closeDocument(doc.Name)
    return geometry_data

# 設定輸入與輸出的檔案路徑
input_step_file = r"C:\0420\CAD教學用(0420累積圖檔)-20260420T014818Z-3-001\CAD教學用(0420累積圖檔)\CAD教學用(累積圖檔)\毛胚\10730888.step"
output_json_file = r"C:\0504上課\Json檔案處理教學-20260504T011509Z-3-001\Json檔案處理教學\geometry_data.json"  # 你可以改成想要的儲存位置與檔名

# 執行提取
data = extract_basic_geometry(input_step_file)

# 判斷是否成功提取並輸出 JSON
if data:
    # 使用 with open 寫入 json 檔案，indent=4 會讓輸出的格式排版整齊易讀
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"資料已成功輸出至: {output_json_file}")
else:
    print("無法提取幾何資料或檔案讀取失敗。")