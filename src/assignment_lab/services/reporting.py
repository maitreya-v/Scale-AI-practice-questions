from ..repositories.catalog import Catalog


def assignment_rows(catalog: Catalog) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for project in catalog.projects.values():
        rows.append({
            "project_id": project.id,
            "assigned": list(project.assigned_contributor_ids),
            "remaining": project.capacity - len(project.assigned_contributor_ids),
        })
    return sorted(rows, key=lambda row: str(row["project_id"]))
