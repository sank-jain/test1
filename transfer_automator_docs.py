from github import Github
import os
import shutil
import pybase64
import PIL
import requests
import io

repo = "activepieces/activepieces"
docs_path_in_repo = "docs/getting-started"
resource_path_in_repo = "docs/resources"
resource_path = "/Users/sanjain15/Desktop/odin-ai-guides/static/resources" # your resource path
odin_docs_path = "/Users/sanjain15/Desktop/odin-ai-guides/docs/" # your docs path
original_activepieces_path = odin_docs_path+"original_docs" # your original activepieces path
converted_activepieces_path = odin_docs_path+"converted_to_odin_automator_docs" # your converted activepieces path

g = Github('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') # put your personal access token here

repo = g.get_repo(repo)

if os.path.exists(original_activepieces_path):
  shutil.rmtree(original_activepieces_path)
os.makedirs(original_activepieces_path)
os.makedirs(original_activepieces_path+"/resources")
os.makedirs(original_activepieces_path+"/getting-started")

if os.path.exists(converted_activepieces_path):
  shutil.rmtree(converted_activepieces_path)
os.makedirs(converted_activepieces_path)
os.makedirs(converted_activepieces_path+"/resources")
os.makedirs(converted_activepieces_path+"/getting-started")

for path in [docs_path_in_repo, resource_path_in_repo]:
    contents = repo.get_contents(path)
    while len(contents) > 1:
        file_content = contents.pop(0)
        print(file_content)
        if file_content.type == "dir":
            try:
                os.makedirs(original_activepieces_path+file_content.path[4:])
                os.makedirs(converted_activepieces_path+file_content.path[4:])
                contents.extend(repo.get_contents(file_content.path))
            except Exception as e:
                print("skipped",file_content.path, e)
        else:
            ext = file_content.path.split(".")[-1]
            try:
                if ext not in ["png", "jpg", "jpeg", "gif", "mp4"]:
                    md_content = repo.get_contents(file_content.path).decoded_content
                    md_content = md_content.decode()
                    with open(original_activepieces_path+file_content.path[4:], 'w') as f:
                        f.write(md_content)
                    with open(converted_activepieces_path+file_content.path[4:], 'w') as f:
                        f.write(md_content.replace("Activepieces", "Odin Automator").replace("activepieces", "Odin Automator").replace("Active pieces", "Odin Automator").replace("active pieces", "Odin Automator"))
                else:
                    try:
                        url = f"https://raw.githubusercontent.com/{repo}/main/{file_content.path}" #file_content.path
                        r = requests.get(url, timeout=4.0)
                        with PIL.Image.open(io.BytesIO(r.content)) as im:
                            im.save(original_activepieces_path+file_content.path[4:])
                            im.save(converted_activepieces_path+file_content.path[4:])
                    except:
                        rawdata = repo.get_contents(file_content.path).content
                        #decode base64 string data
                        decoded_data=pybase64.b64decode((rawdata))
                        #write the decoded data back to original format in  file
                        img_file = open(converted_activepieces_path+file_content.path[4:], 'wb')
                        img_file.write(decoded_data)
                        img_file.close()
                        img_file = open(original_activepieces_path+file_content.path[4:], 'wb')
                        img_file.write(decoded_data)
                        img_file.close()
            except Exception as e:
                print("skipped",file_content.path, e)

if os.path.exists(resource_path):
  shutil.rmtree(resource_path) 
  shutil.copytree(f"{original_activepieces_path}/resources", resource_path)

