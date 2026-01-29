import { createStore } from "/js/AlpineStore.js";

const model = {
  searchQuery: "",
  projectFilter: "all",
  sortBy: "newest",
  closePromise: null,

  async open() {
    this.searchQuery = "";
    this.projectFilter = "all";
    this.sortBy = "newest";

    this.closePromise = window.openModal(
      "modals/chat-browser/chat-browser.html"
    );

    await this.closePromise;
    this.closePromise = null;
  },

  handleClose() {
    window.closeModal();
  },

  get allChats() {
    const chatsStore = Alpine.store("chats");
    if (!chatsStore || !chatsStore.contexts) return [];
    return chatsStore.contexts;
  },

  get uniqueProjects() {
    const projects = [];
    const seen = new Set();
    for (const ctx of this.allChats) {
      const name = ctx.project?.name;
      if (name && !seen.has(name)) {
        seen.add(name);
        projects.push({
          name: name,
          title: ctx.project.title || name,
          color: ctx.project.color || null,
        });
      }
    }
    projects.sort((a, b) => a.title.localeCompare(b.title));
    return projects;
  },

  get filteredChats() {
    let chats = [...this.allChats];

    // Search filter
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      chats = chats.filter((ctx) => {
        const name = ctx.name || "Chat #" + ctx.no;
        return name.toLowerCase().includes(q);
      });
    }

    // Project filter
    if (this.projectFilter === "none") {
      chats = chats.filter((ctx) => !ctx.project?.name);
    } else if (this.projectFilter !== "all") {
      chats = chats.filter(
        (ctx) => ctx.project?.name === this.projectFilter
      );
    }

    // Sort
    switch (this.sortBy) {
      case "newest":
        chats.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
        break;
      case "oldest":
        chats.sort((a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0));
        break;
      case "name-asc":
        chats.sort((a, b) => {
          const na = a.name || "Chat #" + a.no;
          const nb = b.name || "Chat #" + b.no;
          return na.localeCompare(nb);
        });
        break;
      case "name-desc":
        chats.sort((a, b) => {
          const na = a.name || "Chat #" + a.no;
          const nb = b.name || "Chat #" + b.no;
          return nb.localeCompare(na);
        });
        break;
    }

    return chats;
  },

  get totalCount() {
    return this.allChats.length;
  },

  get filteredCount() {
    return this.filteredChats.length;
  },

  formatDate(isoStr) {
    if (!isoStr) return "";
    const date = new Date(isoStr);
    if (isNaN(date.getTime())) return "";
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  },

  selectChat(id) {
    const chatsStore = Alpine.store("chats");
    if (chatsStore) {
      chatsStore.selectChat(id);
    }
    this.handleClose();
  },
};

export const store = createStore("chatBrowser", model);
