import os
import django

# 告訴腳本 Django 的設定檔在哪裡
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quiz_app.models import Question, Choice

def run_import():
    # 執行前先清空題庫，避免重複匯入
    Question.objects.all().delete()
    
    questions_data = [
        # ==========================================
        # 官方原始題庫 (共 11 題，答案請務必在後台再核對一次)
        # ==========================================
        {
            "text": "「單向鏈結串列」的插入，下列何者較快？",
            "choices": [("插在最前面", True), ("插在最後面", False), ("插在最前面或最後面會一樣快", False)]
        },
        {
            "text": "「雙向鏈結串列」的插入，下列何者較快？",
            "choices": [("插在最前面", True), ("插在最後面", False), ("插在最前面或最後面會一樣快", False)]
        },
        {
            "text": "「環狀鏈結串列」的插入，下列何者較快？",
            "choices": [("插在最前面", False), ("插在最後面", False), ("插在最前面或最後面會一樣快", True)]
        },
        {
            "text": "下列何者是「單向鏈結串列」的特性？",
            "choices": [
                ("搜尋某一筆資料的時間複雜度為O(1)", False), 
                ("每個節點都有一個指標指向前一個節點", False), 
                ("每個節點都有一個指標指向後一個節點", True), 
                ("走訪是可以從前面往後面，也可以從後面往前面", False)
            ]
        },
        {
            "text": "有關「單向鏈結串列」的基本操作，下列何者的時間複雜度為O(1)？",
            "choices": [("搜尋某單筆資料", False), ("在最前面插入一筆資料", True), ("在最後面插入一筆資料", False), ("在最後面刪除一筆資料", False)]
        },
        {
            "text": "若節點的Python程式為：class Node: def __init__(self, key = None): self.key = key; self.next = None 則鏈結串列可能是下列何者？",
            "choices": [("單向鏈結串列", True), ("雙向鏈結串列", False), ("環狀鏈結串列", False), ("以上皆非", False)]
        },
        {
            "text": "若節點包含 self.prev = None 與 self.next = None。假設鏈結串列分別為：(1) 單向 (2) 雙向 (3) 環狀。則可能是下列何者？",
            "choices": [("1或2", False), ("1或3", False), ("2或3", True), ("1、2或3", False), ("以上皆非", False)]
        },
        {
            "text": "若想在「單向鏈結串列」中插入一個新的節點，則需改變幾個指標？",
            "choices": [("1", False), ("2", True), ("3", False), ("4", False), ("以上皆非", False)]
        },
        {
            "text": "若想在「雙向鏈結串列」中插入一個新的節點，則需改變幾個指標？",
            "choices": [("1", False), ("2", False), ("3", False), ("4", True), ("以上皆非", False)]
        },
        {
            "text": "下列有關Array與Linked List的敘述，何者正確？",
            "choices": [
                ("Linked List的優點是可以直接存取任何一個成員，所以存取速度快", False), 
                ("Array可以用來模擬Linked List，Linked List也可以用來模擬Array", False), 
                ("Linked List的好處是只要宣告指標變數即可，要使用空間時再向系統要求所需空間，所以不會浪費", True), 
                ("Array的優點是Insert、Delete時不需要搬移大量的成員，因此處理較為快速", False)
            ]
        },
        {
            "text": "下列排序演算法中，何者在平均情形下的排序速度最快？",
            "choices": [("泡沫排序", False), ("插入排序", False), ("合併排序", False), ("快速排序", True), ("桶子排序", False)]
        },
        
        # ==========================================
        # 全新擴充原創題庫 (共 5 題)
        # ==========================================
        {
            "text": "若想在一個長度為 n 的「單向鏈結串列」中讀取第 k 個節點（1 ≤ k ≤ n）的資料，在最壞情況下的時間複雜度為何？",
            "choices": [("O(1)", False), ("O(log n)", False), ("O(n)", True), ("O(n^2)", False)]
        },
        {
            "text": "實作鏈結串列時，工程師經常會在最前方加入一個不儲存實際資料的「虛擬頭節點 (Dummy Head)」，其主要目的為何？",
            "choices": [
                ("節省記憶體的儲存空間", False), 
                ("簡化在串列頭部進行插入與刪除時的邊界條件判斷", True), 
                ("提升尋找特定資料的執行速度", False), 
                ("將單向鏈結串列自動轉為雙向結構", False)
            ]
        },
        {
            "text": "假設有一個長度為 n 的「單向鏈結串列」，且我們「同時擁有」指向頭節點與尾節點的指標。若想要「刪除該尾節點」，其時間複雜度為何？",
            "choices": [("O(1)", False), ("O(log n)", False), ("O(n)", True), ("O(n log n)", False)]
        },
        {
            "text": "在鏈結串列的演算法中，常使用「快慢指標 (一個每次走一步、一個每次走兩步)」。此技巧最主要用來解決什麼問題？",
            "choices": [
                ("將串列內部的資料由大到小排序", False), 
                ("合併兩個已經排序好的串列", False), 
                ("將整條鏈結串列反轉", False), 
                ("判斷鏈結串列中是否包含無窮迴圈 (Cycle)", True)
            ]
        },
        {
            "text": "當我們使用指標 curr 走訪一個「環狀單向鏈結串列」時，若要確認是否已經繞完一圈回到起點，判斷的結束條件通常為下列何者？（假設起始節點為 head）",
            "choices": [("curr.next == Null", False), ("curr.next == head", True), ("curr == Null", False), ("curr.prev == head", False)]
        }
    ]

    # 自動寫入資料庫
    for q_data in questions_data:
        question = Question.objects.create(text=q_data["text"])
        for choice_text, is_correct in q_data["choices"]:
            Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
            
    print(f"✅ 成功匯入 {len(questions_data)} 道題目（含11題原始題庫與5題原創題）與所有對應的選項！")

if __name__ == '__main__':
    run_import()