from src.models.file import File
from pathlib import Path
from pypdf import PdfReader
import docx
from src.helpers.config import get_settings
from src.helpers.id_generator import generate_id
from src.models.data_chunk import DataChunk 
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentService:

    
        def process_file(self,file:File):
            config=get_settings()

            text=self.extract_text(file)

            if text:
                chunks=self.chunk_text(text,file.file_id,file.project_id,config.CHUNK_SIZE,config.CHUNK_OVERLAP)
                return chunks
            return None  
              

        def extract_text(self,file:File):
            path = Path(file.path)
            file_extension=Path(file.file_name).suffix.lower().lstrip(".")

            if file_extension=="txt":
              return  self._extract_text(path)

            elif file_extension=="pdf":
              return  self._extract_pdf(path)

            elif file_extension=="docx":
              return self._extract_docx(path)  

            return None         

        

        def _extract_text(self, path:Path):
        
            text = path.read_text(encoding="utf-8")
            return text
        

        def _extract_pdf(self, path:Path):
        
            reader = PdfReader(str(path))
            text = ""
        
            # Iterate through all pages and extract text
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                    
            return text

        def _extract_docx(self, path:Path):
        
            doc = docx.Document(str(path))
        
            # Connect all paragraphs with a newline character
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
                
            return '\n'.join(full_text)


        def chunk_text(self, text, file_id, project_id, chunk_size: int, overlap: int):
            
            data_chunk_list = []

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
            )

            chunks = splitter.split_text(text)

            for i, text_chunk in enumerate(chunks):
                chunk_id = generate_id()

                data_chunk = DataChunk(
                    chunk_id=chunk_id,
                    file_id=file_id,
                    project_id=project_id,
                    text=text_chunk,
                    chunk_index=i
                )

                data_chunk_list.append(data_chunk)

            return data_chunk_list





