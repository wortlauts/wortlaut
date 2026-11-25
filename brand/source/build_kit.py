"""Rebuilds the whole brand kit: logos, icons, social images, tokens, fonts, README.md, OVERVIEW.html and OVERVIEW.pdf."""
import build_assets

if __name__ == "__main__":
    build_assets.build()   # writes logo/, icon/, social/, tokens/, fonts/
    import build_docs      # noqa: F401  (writes README.md, OVERVIEW.html, OVERVIEW.pdf on import)
    print("done")
