import io, json, csv
from uuid import UUID, uuid4
from typing import Tuple
from services.storage.supabase_client import get_supabase_client

BUCKET = "healthiq-exports"

class ExportService:
    def __init__(self):
        self.client = get_supabase_client()

    def generate_and_upload(
        self,
        *,
        result_dto: dict,
        user_id: UUID,
        analysis_id: UUID,
        fmt: str
    ) -> Tuple[str, int]:
        fmt = fmt.lower()
        export_id = uuid4()
        if fmt == "json":
            content_bytes = json.dumps(result_dto, ensure_ascii=False, indent=2, default=str).encode("utf-8")
            ext = "json"
            content_type = "application/json"
        elif fmt == "csv":
            content_bytes = self._to_csv_bytes(result_dto)
            ext = "csv"
            content_type = "text/csv"
        else:
            raise ValueError(f"Unsupported format: {fmt}")

        storage_path = f"exports/{user_id}/{analysis_id}/{export_id}.{ext}"

        # Upload
        self.client.storage.from_(BUCKET).upload(
            path=storage_path,
            file=content_bytes,
            file_options={"contentType": content_type}
        )

        return storage_path, len(content_bytes)

    def signed_url(self, storage_path: str, ttl_seconds: int = 7 * 24 * 60 * 60) -> str:
        res = self.client.storage.from_(BUCKET).create_signed_url(path=storage_path, expires_in=ttl_seconds)
        return res["signedURL"]

    def _to_csv_bytes(self, result_dto: dict) -> bytes:
        """
        CSV columns aligned to our DTO:
        biomarker_name, value, unit, status, reference_min, reference_max
        """
        output = io.StringIO()
        w = csv.writer(output)
        w.writerow(["biomarker_name", "value", "unit", "status", "reference_min", "reference_max"])
        biomarkers = result_dto.get("biomarkers", []) or []
        for bm in biomarkers:
            name = bm.get("biomarker_name")
            value = bm.get("value")
            unit = bm.get("unit")
            status = bm.get("status")
            ref = bm.get("reference_range") or {}
            ref_min = ref.get("min")
            ref_max = ref.get("max")
            w.writerow([name, value, unit, status, ref_min, ref_max])
        return output.getvalue().encode("utf-8")
